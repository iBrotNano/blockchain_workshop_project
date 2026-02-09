from address.address import Address
from project.project import Project
from project.merkle_root import MerkleRoot
from project.command_line import CommandLine
from config.console import console
from address.custom_address import CustomAddress as CustomAddress
from address.solana_address import SolanaAddress as SolanaAddress

custom_address = CustomAddress("Custom", Address.generate_mnemonic())
console.print(f"Generated custom address: {custom_address.get_address()}")
console.print(f"Public key (raw, hex): {custom_address.get_pubkey()}")
console.print(f"Mnemonic: {custom_address.get_mnemonic()}")
console.print(custom_address.get_keypair())
custom_address.save()
loaded = custom_address.load(custom_address.name)
console.print(f"Loaded custom address: {loaded.get_address()}")
console.print(f"Public key (raw, hex): {loaded.get_pubkey()}")
console.print(f"Mnemonic: {loaded.get_mnemonic()}")
console.print(loaded.get_keypair())

solana_address = SolanaAddress("Solana", Address.generate_mnemonic())
console.print(f"Generated Solana address: {solana_address.get_address()}")
console.print(f"Public key (raw, hex): {solana_address.get_pubkey()}")
console.print(f"Mnemonic: {solana_address.get_mnemonic()}")
console.print(solana_address.get_keypair())
solana_address.save()
loaded = solana_address.load(solana_address.name)
console.print(f"Loaded Solana address: {loaded.get_address()}")
console.print(f"Public key (raw, hex): {loaded.get_pubkey()}")
console.print(f"Mnemonic: {loaded.get_mnemonic()}")
console.print(loaded.get_keypair())

# project_cli = CommandLine()
# project = Project(project_cli.select_project_path())
# merkle_root = MerkleRoot(project)
# merkle_root.compute_root()
# project_cli.display_merkle_root(merkle_root)
