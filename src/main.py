from project.project import Project
from project.merkle_root import MerkleRoot
from project.command_line import CommandLine
from config.console import console
from address.address import Address

address = Address()
console.print(f"Generated address: {address.address}")
console.print(f"Public key (raw, hex): {address.public_key}")
console.print(f"Private key (raw, hex): {address.private_key}")
# project_cli = CommandLine()
# project = Project(project_cli.select_project_path())
# merkle_root = MerkleRoot(project)
# merkle_root.compute_root()
# project_cli.display_merkle_root(merkle_root)
