import requests
from colorama import Fore, Style

def format_total_supply(total_supply):
    if total_supply.isdigit():
        total_supply = int(total_supply)
    else:
        return "Unknown"
    
    if total_supply == 0:
        return "M"
    
    suffixes = ["", "K", "M", "B", "T"]
    magnitude = 0
    while total_supply >= 1000:
        total_supply /= 1000.0
        magnitude += 1
    if magnitude >= len(suffixes):
        magnitude = len(suffixes) - 1
    return f"{total_supply:.1f}{suffixes[magnitude]}"


def check_contract_safety(contract_address):

    # Memeriksa informasi token
    token_info_url = f'https://explorer.degen.tips/api/v2/tokens/{contract_address}'
    token_info_response = requests.get(token_info_url)
    if token_info_response.status_code == 200:
        token_info = token_info_response.json()
        token_name = token_info.get('name', 'Unknown Token')
        token_symbol = token_info.get('symbol', 'Unknown Symbol')
        holders_count = token_info.get('holders', 'Unknown')
        total_supply = token_info.get('total_supply', 'Unknown')
        
        # Format total supply
        total_supply_formatted = format_total_supply(total_supply)

        print(f"{Fore.CYAN}Token Name: {token_name} ({token_symbol})")
        print(f"Holders: {holders_count}")
        print(f"Total Supply: {total_supply_formatted}{Style.RESET_ALL}")
    else:
        print("Failed to load token information.")

    # Memeriksa informasi kontrak
    contract_info_url = f'https://explorer.degen.tips/api/v2/smart-contracts/{contract_address}'
    contract_info_response = requests.get(contract_info_url)
    if contract_info_response.status_code == 200:
        contract_info = contract_info_response.json()
        contract_name = contract_info.get('name', 'Unknown Contract')
        is_verified = contract_info.get('is_verified', False)
        is_partially_verified = contract_info.get('is_partially_verified', False)
        abi = contract_info.get('abi', [])

        if is_verified:
            print(f"{Fore.GREEN}{contract_name} Contract has been verified.")
        elif is_partially_verified:
            print(f"{Fore.YELLOW}{contract_name} Contract partially verified.")
        else:
            print(f"{Fore.RED}{contract_name}. Never buy unknown contract/unverified contract!")
            return 

        honeypot_found = False
        
        for func in abi:
            if 'name' in func:
                func_name = func['name']
            else:
                func_name = 'Unknown Function'
                
            state_mutability = func.get('stateMutability', '')
            modifiers = func.get('modifiers', []) 
            if state_mutability == 'nonpayable' and not modifiers:
                pass
            else:
                honeypot_found = True
        
        if honeypot_found:
            print(f"{Fore.RED}Probably Honeypot or Not Safe{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Good{Style.RESET_ALL}")
    else:
        print("Failed to load Contract Address.")

contract_address = input("Please Input Contract Address: ")
check_contract_safety(contract_address)
