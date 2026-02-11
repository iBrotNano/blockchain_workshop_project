from pathlib import Path
from address.custom_address import CustomAddress
from config.config import DEPLOYMENT_RECORD_VERSION
from project.merkle_root import MerkleRoot
from project.deployment_record import DeploymentRecord
from project.project import Project


def test_serialize_is_deterministic():
    mnemonic = CustomAddress.generate_mnemonic()
    address = CustomAddress("Test", mnemonic)
    project = Project(Path("."))
    merkle_root = MerkleRoot(project)

    metadata = {
        "author": "Marcel",
        "contact_info": "developer666@gmail.com",
        "software_name": "Plockchain",
        "version": "1.0.0",
        "commit_hash": "7cff475efd3f13e2b637f20d8187a3ccddb24efc",
        "repository_url": "https://github.com/iBrotNano/blockchain_workshop_project/commit/7cff475efd3f13e2b637f20d8187a3ccddb24efc",
        "timestamp": "2026-02-11T10:39:41",
    }

    record1 = DeploymentRecord(address, merkle_root, metadata)
    serialized1, signature1 = record1.serialize()
    record2 = DeploymentRecord(address, merkle_root, metadata)
    serialized2, signature2 = record2.serialize()
    assert serialized1 == serialized2
    assert signature1 == signature2
