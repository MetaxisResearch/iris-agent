"""
P2MR Session Identity for Iris.

Each Iris session can optionally generate a P2MR address that
acts as a quantum-resistant identity commitment for that session.
The Merkle tree is built from the session's active skills and
context files — binding agent capability to a verifiable on-chain root.

This means a session's scope is cryptographically committed.
Anyone can verify what scripts (skills) Iris was running in a
given session without exposing any public key.
"""

import hashlib
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from tools.bip360 import (
    generate_p2mr_address,
    build_merkle_tree,
    MerkleLeaf,
    P2MRAddress,
    verify_merkle_proof,
)


@dataclass
class SessionCommitment:
    session_id: str
    address: str
    merkle_root: str
    skills_committed: list[str]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    network: str = "testnet"

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "p2mr_address": self.address,
            "merkle_root": self.merkle_root,
            "skills": self.skills_committed,
            "timestamp": self.timestamp,
            "network": self.network,
        }


class P2MRSessionManager:
    """
    Manages quantum-resistant session identity for Iris.

    On session start, builds a Merkle tree from the active skill
    set and generates a P2MR address. This address uniquely
    identifies this session's capability scope in a way that
    survives quantum attack — no public key is ever exposed.

    Usage:
        manager = P2MRSessionManager(session_id="abc123")
        commitment = manager.commit_session(active_skills=["pqc-monitor", "web-search"])
        print(commitment.address)  # tb1z...
    """

    def __init__(self, session_id: str, network: str = "testnet"):
        self.session_id = session_id
        self.network = network
        self._commitment: Optional[SessionCommitment] = None

    def _skill_to_script(self, skill_name: str) -> bytes:
        """
        Deterministically encode a skill name as a script leaf.
        Uses tagged hash so each skill produces a unique 32-byte leaf.
        """
        tag = f"IrisSkill/v1/{skill_name}"
        tag_hash = hashlib.sha256(tag.encode()).digest()
        payload = hashlib.sha256(
            tag_hash + tag_hash + self.session_id.encode()
        ).digest()
        # OP_RETURN style: push the 32-byte payload as a script
        return bytes([0x6A, 0x20]) + payload

    def commit_session(self, active_skills: list[str]) -> SessionCommitment:
        """
        Build a P2MR commitment from the current session's active skills.
        Each skill becomes a leaf in the Merkle tree.
        Returns a SessionCommitment with the resulting bc1z address.
        """
        if not active_skills:
            active_skills = ["default"]

        scripts = [self._skill_to_script(s) for s in active_skills]
        addr = generate_p2mr_address(scripts, network=self.network)
        leaves = [MerkleLeaf(script=s) for s in scripts]
        root = build_merkle_tree(leaves)

        self._commitment = SessionCommitment(
            session_id=self.session_id,
            address=str(addr),
            merkle_root=root.hex(),
            skills_committed=active_skills,
            network=self.network,
        )
        return self._commitment

    def verify_skill_in_session(self, skill_name: str, proof: list[bytes]) -> bool:
        """
        Verify that a specific skill was committed in this session's
        P2MR address without revealing any other skills.
        """
        if not self._commitment:
            raise RuntimeError("Session not committed yet. Call commit_session first.")

        leaf = MerkleLeaf(script=self._skill_to_script(skill_name))
        root_bytes = bytes.fromhex(self._commitment.merkle_root)
        return verify_merkle_proof(leaf, proof, root_bytes)

    def export(self) -> str:
        if not self._commitment:
            return "{}"
        return json.dumps(self._commitment.to_dict(), indent=2)
