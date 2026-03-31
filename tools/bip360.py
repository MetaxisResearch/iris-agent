"""
BIP-360 Pay-to-Merkle-Root (P2MR) tool for Iris.
Enables the agent to generate quantum-resistant bc1z addresses,
construct Merkle trees from script leaves, and verify proofs
against committed roots on testnet.
"""

import hashlib
import hmac
import struct
from typing import Optional
from dataclasses import dataclass

# BIP-360 uses bc1z HRP (human-readable part) vs Taproot's bc1p
P2MR_HRP_MAINNET = "bc"
P2MR_HRP_TESTNET = "tb"
P2MR_WITNESS_VERSION = 0x02  # version byte for P2MR (distinct from Taproot v1)

BECH32M_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32M_CONST = 0x2BC830A3


@dataclass
class MerkleLeaf:
    script: bytes
    tag: str = "TapLeaf/P2MR"

    def hash(self) -> bytes:
        tagged = _tagged_hash(self.tag, self.script)
        return tagged


@dataclass
class P2MRAddress:
    merkle_root: bytes
    network: str = "testnet"

    def to_bech32m(self) -> str:
        hrp = P2MR_HRP_TESTNET if self.network == "testnet" else P2MR_HRP_MAINNET
        witness_program = bytes([P2MR_WITNESS_VERSION]) + self.merkle_root
        return _bech32m_encode(hrp, witness_program)

    def __str__(self):
        return self.to_bech32m()


def build_merkle_tree(leaves: list[MerkleLeaf]) -> bytes:
    """
    Build a BIP-341-compatible Merkle tree from script leaves.
    P2MR commits ONLY to this root — no internal key, unlike Taproot.
    Returns the 32-byte Merkle root.
    """
    if not leaves:
        raise ValueError("Cannot build Merkle tree from empty leaf set")

    layer = [leaf.hash() for leaf in leaves]

    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else layer[i]
            combined = _tagged_hash(
                "TapBranch/P2MR",
                (left if left <= right else right) + (right if left <= right else left)
            )
            next_layer.append(combined)
        layer = next_layer

    return layer[0]


def generate_p2mr_address(scripts: list[bytes], network: str = "testnet") -> P2MRAddress:
    """
    Given a list of raw script bytes, generate a P2MR address.
    This is the core BIP-360 operation: no public key is committed,
    only the Merkle root of scripts. Quantum-resistant by design.

    Example usage inside Iris:
        addr = generate_p2mr_address([my_script], network="testnet")
        print(addr)  # tb1z...
    """
    leaves = [MerkleLeaf(script=s) for s in scripts]
    root = build_merkle_tree(leaves)
    return P2MRAddress(merkle_root=root, network=network)


def verify_merkle_proof(
    leaf: MerkleLeaf,
    proof: list[bytes],
    root: bytes,
) -> bool:
    """
    Verify that a script leaf is committed to in a P2MR Merkle root.
    Used to validate spend conditions without exposing a public key.
    """
    current = leaf.hash()
    for sibling in proof:
        left = current if current <= sibling else sibling
        right = sibling if current <= sibling else current
        current = _tagged_hash("TapBranch/P2MR", left + right)
    return hmac.compare_digest(current, root)


def _tagged_hash(tag: str, data: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + data).digest()


def _bech32m_encode(hrp: str, data: bytes) -> str:
    """Encode bytes as bech32m with given HRP."""
    converted = _convertbits(list(data), 8, 5)
    if converted is None:
        raise ValueError("bech32m conversion failed")
    checksum = _bech32m_create_checksum(hrp, converted)
    return hrp + "1" + "".join([BECH32M_CHARSET[d] for d in converted + checksum])


def _bech32m_polymod(values):
    GEN = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def _bech32m_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _bech32m_create_checksum(hrp, data):
    values = _bech32m_hrp_expand(hrp) + list(data)
    polymod = _bech32m_polymod(values + [0, 0, 0, 0, 0, 0]) ^ BECH32M_CONST
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def _convertbits(data, frombits, tobits, pad=True):
    acc, bits, ret, maxv = 0, 0, [], (1 << tobits) - 1
    for value in data:
        acc = ((acc << frombits) | value) & 0xFFFFFFFF
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret
