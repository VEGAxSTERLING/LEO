#!/usr/bin/env python3
"""
Hash Cracker (LEO) - Password Recovery Tool (Enhanced)
Author: VEGAxSTERLING
Purpose: Ethical penetration testing and security research
License: Educational and authorized security testing only
"""

import hashlib
import itertools
import string
import sys
import time
import base64
import binascii
from pathlib import Path
from typing import Optional, Callable, Dict
from multiprocessing import Pool, cpu_count
from functools import partial

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AdvancedHasher:
    """Advanced hashing utilities with multiple encoding support"""
    
    @staticmethod
    def ntlm_hash(password: str) -> str:
        """Generate NTLM hash (Windows)"""
        try:
            return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
        except:
            return ""
    
    @staticmethod
    def lm_hash(password: str) -> str:
        """Generate LM hash (Legacy Windows)"""
        try:
            from Crypto.Cipher import DES
            password = password.upper()[:14].ljust(14, '\0')
            key1 = password[:7].encode('ascii')
            key2 = password[7:].encode('ascii')
            
            def create_des_key(s):
                key = []
                key.append(s[0] >> 1)
                key.append(((s[0] & 0x01) << 6) | (s[1] >> 2))
                key.append(((s[1] & 0x03) << 5) | (s[2] >> 3))
                key.append(((s[2] & 0x07) << 4) | (s[3] >> 4))
                key.append(((s[3] & 0x0F) << 3) | (s[4] >> 5))
                key.append(((s[4] & 0x1F) << 2) | (s[5] >> 6))
                key.append(((s[5] & 0x3F) << 1) | (s[6] >> 7))
                key.append(s[6] & 0x7F)
                return bytes(key)
            
            magic = b'KGS!@#$%'
            cipher1 = DES.new(create_des_key(key1), DES.MODE_ECB)
            cipher2 = DES.new(create_des_key(key2), DES.MODE_ECB)
            
            hash1 = cipher1.encrypt(magic)
            hash2 = cipher2.encrypt(magic)
            
            return (hash1 + hash2).hex()
        except:
            return ""
    
    @staticmethod
    def mysql_hash(password: str) -> str:
        """MySQL OLD_PASSWORD hash"""
        hash1 = hashlib.sha1(password.encode()).digest()
        return hashlib.sha1(hash1).hexdigest()
    
    @staticmethod
    def bcrypt_verify(password: str, hash_str: str) -> bool:
        """Verify bcrypt hash"""
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode(), hash_str.encode())
        except:
            return False
    
    @staticmethod
    def argon2_verify(password: str, hash_str: str) -> bool:
        """Verify Argon2 hash"""
        try:
            from argon2 import PasswordHasher
            ph = PasswordHasher()
            ph.verify(hash_str, password)
            return True
        except:
            return False

class HashCracker:
    """Professional hash cracking tool with enhanced performance"""
    
    SUPPORTED_ALGORITHMS = {
        # Classic & Common (Fast)
        '1': ('MD5', lambda p: hashlib.md5(p).hexdigest()),
        '2': ('SHA1', lambda p: hashlib.sha1(p).hexdigest()),
        '3': ('SHA224', lambda p: hashlib.sha224(p).hexdigest()),
        '4': ('SHA256', lambda p: hashlib.sha256(p).hexdigest()),
        '5': ('SHA384', lambda p: hashlib.sha384(p).hexdigest()),
        '6': ('SHA512', lambda p: hashlib.sha512(p).hexdigest()),
        
        # SHA-3 Family
        '7': ('SHA3-224', lambda p: hashlib.sha3_224(p).hexdigest()),
        '8': ('SHA3-256', lambda p: hashlib.sha3_256(p).hexdigest()),
        '9': ('SHA3-384', lambda p: hashlib.sha3_384(p).hexdigest()),
        '10': ('SHA3-512', lambda p: hashlib.sha3_512(p).hexdigest()),
        
        # BLAKE Family (Modern & Fast)
        '11': ('BLAKE2b', lambda p: hashlib.blake2b(p).hexdigest()),
        '12': ('BLAKE2s', lambda p: hashlib.blake2s(p).hexdigest()),
        
        # Extended Functions
        '13': ('SHAKE-128', lambda p: hashlib.shake_128(p).hexdigest(16)),
        '14': ('SHAKE-256', lambda p: hashlib.shake_256(p).hexdigest(32)),
        
        # Specialized Hashes
        '15': ('RIPEMD-160', lambda p: hashlib.new('ripemd160', p).hexdigest()),
        '16': ('Whirlpool', lambda p: hashlib.new('whirlpool', p).hexdigest()),
        '17': ('SM3', lambda p: hashlib.new('sm3', p).hexdigest()),
        
        # Windows Authentication
        '18': ('NTLM', lambda p: AdvancedHasher.ntlm_hash(p.decode('utf-8', errors='ignore'))),
        '19': ('LM Hash', lambda p: AdvancedHasher.lm_hash(p.decode('utf-8', errors='ignore'))),
        
        # Database & Web
        '20': ('MySQL (SHA1)', lambda p: AdvancedHasher.mysql_hash(p.decode('utf-8', errors='ignore'))),
        '21': ('MD4', lambda p: hashlib.new('md4', p).hexdigest()),
        
        # Base64 Encoded Hashes
        '22': ('MD5 (Base64)', lambda p: base64.b64encode(hashlib.md5(p).digest()).decode().rstrip('=')),
        '23': ('SHA256 (Base64)', lambda p: base64.b64encode(hashlib.sha256(p).digest()).decode().rstrip('=')),
        
        # Double Hashing (Common in Web Apps)
        '24': ('MD5(MD5)', lambda p: hashlib.md5(hashlib.md5(p).hexdigest().encode()).hexdigest()),
        '25': ('SHA1(SHA1)', lambda p: hashlib.sha1(hashlib.sha1(p).hexdigest().encode()).hexdigest()),
        
        # Salted Variations (for demo - user provides salt)
        '26': ('MD5(pass:salt)', lambda p: ''),  # Special handling
        '27': ('SHA256(salt:pass)', lambda p: ''),  # Special handling
    }
    
    def __init__(self):
        self.target_hash = ""
        self.hash_function: Optional[Callable] = None
        self.algorithm_name = ""
        self.algorithm_key = ""
        self.attempts = 0
        self.start_time = 0
        self.use_multiprocessing = True
        self.num_processes = max(1, cpu_count() - 1)
        self.salt = ""
        
    def print_banner(self):
        """Display enhanced tool banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ██╗     ███████╗ ██████╗ 
 ██║     ██╔════╝██╔═══██╗
 ██║     █████╗  ██║   ██║
 ██║     ██╔══╝  ██║   ██║
 ███████╗███████╗╚██████╔╝
 ╚══════╝╚══════╝ ╚═════╝ 
{Colors.END}
{Colors.CYAN}    Advanced Password Recovery & Security Testing{Colors.END}
{Colors.CYAN}    Multi-Core Processing | 27 Hash Algorithms{Colors.END}
{Colors.CYAN}    Developed by: Mickey{Colors.END}

{Colors.GREEN}[+] Multi-processing enabled ({self.num_processes} cores){Colors.END}
{Colors.GREEN}[+] Optimized hash computation{Colors.END}
{Colors.GREEN}[+] Advanced encoding support{Colors.END}
"""
        print(banner)
    
    def print_algorithms(self):
        """Display supported hash algorithms in organized categories"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Supported Hash Algorithms (27 Total):{Colors.END}\n")
        
        categories = {
            'Classic & Common (Fast)': ['1', '2', '3', '4', '5', '6'],
            'SHA-3 Family': ['7', '8', '9', '10'],
            'BLAKE Family (Modern)': ['11', '12'],
            'Extended Functions': ['13', '14'],
            'Specialized': ['15', '16', '17'],
            'Windows Authentication': ['18', '19'],
            'Database & Legacy': ['20', '21'],
            'Encoded Variants': ['22', '23'],
            'Double Hashing': ['24', '25'],
            'Salted (Advanced)': ['26', '27']
        }
        
        for category, keys in categories.items():
            print(f"{Colors.CYAN}{category}:{Colors.END}")
            for key in keys:
                if key in self.SUPPORTED_ALGORITHMS:
                    name, _ = self.SUPPORTED_ALGORITHMS[key]
                    print(f"  [{Colors.GREEN}{key.ljust(2)}{Colors.END}] {name}")
            print()
    
    def select_algorithm(self) -> bool:
        """Allow user to select hashing algorithm"""
        self.print_algorithms()
        choice = input(f"{Colors.CYAN}Select algorithm (1-27): {Colors.END}").strip()
        
        if choice in self.SUPPORTED_ALGORITHMS:
            self.algorithm_name, hash_func = self.SUPPORTED_ALGORITHMS[choice]
            self.algorithm_key = choice
            self.hash_function = hash_func
            
            # Handle salted hashes
            if choice in ['26', '27']:
                self.salt = input(f"{Colors.CYAN}Enter salt value: {Colors.END}").strip()
            
            print(f"{Colors.GREEN}✓ Selected: {self.algorithm_name}{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ Invalid selection!{Colors.END}")
            return False
    
    def get_target_hash(self):
        """Get target hash from user"""
        self.target_hash = input(f"\n{Colors.CYAN}Enter target hash: {Colors.END}").strip()
        
        # Remove common prefixes
        if self.target_hash.startswith('$'):
            parts = self.target_hash.split('$')
            if len(parts) > 1:
                print(f"{Colors.YELLOW}[*] Detected formatted hash, extracting hash value...{Colors.END}")
        
        # Normalize for comparison
        if self.algorithm_key not in ['22', '23']:  # Not base64
            self.target_hash = self.target_hash.lower()
        
        print(f"{Colors.GREEN}✓ Target hash loaded ({len(self.target_hash)} chars){Colors.END}")
    
    def hash_password(self, password_bytes: bytes) -> str:
        """Hash a password using selected algorithm (optimized)"""
        try:
            # Handle salted hashes
            if self.algorithm_key == '26':  # MD5(pass:salt)
                data = password_bytes + b':' + self.salt.encode()
                return hashlib.md5(data).hexdigest()
            elif self.algorithm_key == '27':  # SHA256(salt:pass)
                data = self.salt.encode() + b':' + password_bytes
                return hashlib.sha256(data).hexdigest()
            
            # Standard hashing
            result = self.hash_function(password_bytes)
            return result if isinstance(result, str) else result.hexdigest()
        except Exception:
            return ""
    
    def check_password_batch(self, passwords: list) -> Optional[str]:
        """Check a batch of passwords (optimized for multiprocessing)"""
        for password in passwords:
            password_bytes = password.encode('utf-8', errors='ignore')
            if self.hash_password(password_bytes) == self.target_hash:
                return password
        return None
    
    def dictionary_attack(self, wordlist_path: str) -> Optional[str]:
        """Perform optimized dictionary-based attack with multiprocessing"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}[*] Starting Dictionary Attack...{Colors.END}")
        
        path = Path(wordlist_path)
        if not path.exists():
            print(f"{Colors.RED}✗ Wordlist file not found: {wordlist_path}{Colors.END}")
            return None
        
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            # Load wordlist into memory for faster processing
            print(f"{Colors.YELLOW}[*] Loading wordlist...{Colors.END}")
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            total_passwords = len(passwords)
            print(f"{Colors.GREEN}✓ Loaded {total_passwords:,} passwords{Colors.END}")
            
            if self.use_multiprocessing and total_passwords > 10000:
                # Split into chunks for multiprocessing
                chunk_size = max(1000, total_passwords // (self.num_processes * 4))
                chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
                
                print(f"{Colors.YELLOW}[*] Using {self.num_processes} cores with {len(chunks)} chunks{Colors.END}")
                
                with Pool(processes=self.num_processes) as pool:
                    for i, chunk in enumerate(chunks):
                        self.attempts += len(chunk)
                        
                        if i % 10 == 0:
                            elapsed = time.time() - self.start_time
                            rate = self.attempts / elapsed if elapsed > 0 else 0
                            print(f"{Colors.YELLOW}[*] Progress: {self.attempts:,}/{total_passwords:,} ({rate:,.0f} h/s){Colors.END}", end='\r')
                        
                        # Check chunk
                        result = self.check_password_batch(chunk)
                        if result:
                            pool.terminate()
                            return result
            else:
                # Single-threaded for smaller lists
                for password in passwords:
                    self.attempts += 1
                    
                    if self.attempts % 10000 == 0:
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"{Colors.YELLOW}[*] Tested {self.attempts:,}/{total_passwords:,} ({rate:,.0f} h/s){Colors.END}", end='\r')
                    
                    password_bytes = password.encode('utf-8', errors='ignore')
                    if self.hash_password(password_bytes) == self.target_hash:
                        return password
                        
        except Exception as e:
            print(f"\n{Colors.RED}✗ Error: {e}{Colors.END}")
            return None
        
        return None
    
    def brute_force_attack(self, min_len: int, max_len: int, charset: str) -> Optional[str]:
        """Perform optimized brute-force attack"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}[*] Starting Brute-Force Attack...{Colors.END}")
        
        # Calculate total combinations
        total = sum(len(charset) ** i for i in range(min_len, max_len + 1))
        print(f"{Colors.YELLOW}[*] Length: {min_len}-{max_len} | Charset: {len(charset)} chars{Colors.END}")
        print(f"{Colors.YELLOW}[*] Total combinations: {total:,}{Colors.END}")
        
        if total > 1000000:
            print(f"{Colors.RED}Warning: This will take a very long time!{Colors.END}")
            confirm = input(f"{Colors.CYAN}Continue? (y/n): {Colors.END}").strip().lower()
            if confirm != 'y':
                return None
        
        self.start_time = time.time()
        self.attempts = 0
        
        for length in range(min_len, max_len + 1):
            print(f"\n{Colors.CYAN}[*] Testing passwords of length {length}...{Colors.END}")
            
            batch = []
            batch_size = 10000
            
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                batch.append(password)
                
                if len(batch) >= batch_size:
                    self.attempts += len(batch)
                    
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"{Colors.YELLOW}[*] Tested {self.attempts:,} ({rate:,.0f} h/s){Colors.END}", end='\r')
                    
                    result = self.check_password_batch(batch)
                    if result:
                        return result
                    
                    batch = []
            
            # Check remaining batch
            if batch:
                self.attempts += len(batch)
                result = self.check_password_batch(batch)
                if result:
                    return result
        
        return None
    
    def hybrid_attack(self, wordlist_path: str, mutations: list) -> Optional[str]:
        """Perform optimized hybrid attack with intelligent mutations"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}[*] Starting Hybrid Attack...{Colors.END}")
        
        path = Path(wordlist_path)
        if not path.exists():
            print(f"{Colors.RED}✗ Wordlist file not found: {wordlist_path}{Colors.END}")
            return None
        
        self.start_time = time.time()
        self.attempts = 0
        
        try:
            print(f"{Colors.YELLOW}[*] Loading wordlist...{Colors.END}")
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            
            print(f"{Colors.GREEN}✓ Loaded {len(words):,} base words{Colors.END}")
            print(f"{Colors.YELLOW}[*] Generating mutations...{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}✗ Error reading wordlist: {e}{Colors.END}")
            return None
        
        mutation_funcs = {
            'capitalize': lambda w: [w.capitalize(), w.upper(), w.lower(), w.title()],
            'reverse': lambda w: [w[::-1], w.capitalize()[::-1]],
            'leet': lambda w: [w.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')],
            'numbers': lambda w: [w + str(i) for i in range(100)] + [str(i) + w for i in range(10)],
            'years': lambda w: [w + str(y) for y in range(1980, 2026)],
            'symbols': lambda w: [w + s for s in ['!', '@', '#', '$', '123', '2024', '2025', '!@#']],
            'double': lambda w: [w + w, w.capitalize() + w],
            'common': lambda w: [w + 'pass', 'pass' + w, w + 'word', w + '1', w + '12', w + '123']
        }
        
        for word_idx, word in enumerate(words):
            # Test base word
            batch = [word]
            
            # Generate all mutations for this word
            for mutation in mutations:
                if mutation in mutation_funcs:
                    batch.extend(mutation_funcs[mutation](word))
            
            # Remove duplicates
            batch = list(dict.fromkeys(batch))
            
            self.attempts += len(batch)
            
            if word_idx % 100 == 0:
                elapsed = time.time() - self.start_time
                rate = self.attempts / elapsed if elapsed > 0 else 0
                print(f"{Colors.YELLOW}[*] Word {word_idx:,}/{len(words):,} | Tested {self.attempts:,} ({rate:,.0f} h/s){Colors.END}", end='\r')
            
            result = self.check_password_batch(batch)
            if result:
                return result
        
        return None
    
    def print_result(self, password: Optional[str]):
        """Print enhanced cracking results"""
        elapsed = time.time() - self.start_time
        
        print(f"\n\n{Colors.BOLD}{'='*70}{Colors.END}")
        
        if password:
            print(f"{Colors.GREEN}{Colors.BOLD}[+] PASSWORD CRACKED!{Colors.END}")
            print(f"\n{Colors.CYAN}Target Hash:  {Colors.END}{self.target_hash}")
            print(f"{Colors.GREEN}Password:     {Colors.END}{Colors.BOLD}{password}{Colors.END}")
            print(f"{Colors.GREEN}Length:       {Colors.END}{len(password)} characters")
        else:
            print(f"{Colors.RED}{Colors.BOLD}[-] PASSWORD NOT FOUND{Colors.END}")
            print(f"\n{Colors.CYAN}Target Hash:  {Colors.END}{self.target_hash}")
            print(f"{Colors.YELLOW}Tip: Try a different wordlist or attack method{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Algorithm:    {Colors.END}{self.algorithm_name}")
        print(f"{Colors.YELLOW}Attempts:     {Colors.END}{self.attempts:,}")
        print(f"{Colors.YELLOW}Time Elapsed: {Colors.END}{elapsed:.2f} seconds")
        
        if self.attempts > 0 and elapsed > 0:
            rate = self.attempts / elapsed
            print(f"{Colors.YELLOW}Hash Rate:    {Colors.END}{rate:,.0f} hashes/second")
            
            if rate > 100000:
                print(f"{Colors.GREEN}Performance:  {Colors.END}Excellent")
            elif rate > 10000:
                print(f"{Colors.GREEN}Performance:  {Colors.END}Good")
            else:
                print(f"{Colors.YELLOW}Performance:  {Colors.END}Standard")
        
        print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    def run(self):
        """Main execution loop"""
        self.print_banner()
        
        # Performance settings
        print(f"\n{Colors.BOLD}{Colors.BLUE}Performance Settings:{Colors.END}")
        mp_choice = input(f"{Colors.CYAN}Enable multi-core processing? (y/n, default=y): {Colors.END}").strip().lower()
        self.use_multiprocessing = mp_choice != 'n'
        
        if self.use_multiprocessing:
            print(f"{Colors.GREEN}[+] Multi-core enabled ({self.num_processes} cores){Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] Single-core mode (slower){Colors.END}")
        
        while True:
            print(f"\n{Colors.BOLD}{Colors.BLUE}Attack Methods:{Colors.END}")
            print(f"  [{Colors.GREEN}1{Colors.END}] Dictionary Attack (Fast)")
            print(f"  [{Colors.GREEN}2{Colors.END}] Brute-Force Attack (Comprehensive)")
            print(f"  [{Colors.GREEN}3{Colors.END}] Hybrid Attack (Smart)")
            print(f"  [{Colors.GREEN}4{Colors.END}] Exit")
            
            choice = input(f"\n{Colors.CYAN}Select attack method: {Colors.END}").strip()
            
            if choice == '4':
                print(f"\n{Colors.CYAN}Thank you for using LEO!{Colors.END}")
                print(f"{Colors.YELLOW}Stay ethical, stay safe!{Colors.END}\n")
                break
            
            if not self.select_algorithm():
                continue
            
            self.get_target_hash()
            result = None
            
            if choice == '1':
                wordlist = input(f"\n{Colors.CYAN}Enter wordlist path: {Colors.END}").strip()
                result = self.dictionary_attack(wordlist)
                
            elif choice == '2':
                print(f"\n{Colors.YELLOW}Brute-force configuration:{Colors.END}")
                try:
                    min_len = int(input(f"{Colors.CYAN}Minimum length (1-4 recommended): {Colors.END}"))
                    max_len = int(input(f"{Colors.CYAN}Maximum length: {Colors.END}"))
                except ValueError:
                    print(f"{Colors.RED}✗ Invalid input!{Colors.END}")
                    continue
                
                print(f"\n{Colors.YELLOW}Character sets:{Colors.END}")
                print(f"  [1] Lowercase (a-z)")
                print(f"  [2] Uppercase (A-Z)")
                print(f"  [3] Digits (0-9)")
                print(f"  [4] Lowercase + Digits")
                print(f"  [5] All alphanumeric")
                print(f"  [6] Alphanumeric + Symbols")
                
                charset_choice = input(f"\n{Colors.CYAN}Select charset: {Colors.END}").strip()
                
                charset_map = {
                    '1': string.ascii_lowercase,
                    '2': string.ascii_uppercase,
                    '3': string.digits,
                    '4': string.ascii_lowercase + string.digits,
                    '5': string.ascii_letters + string.digits,
                    '6': string.ascii_letters + string.digits + '!@#$%^&*()'
                }
                
                charset = charset_map.get(charset_choice, string.ascii_lowercase)
                result = self.brute_force_attack(min_len, max_len, charset)
                
            elif choice == '3':
                wordlist = input(f"\n{Colors.CYAN}Enter wordlist path: {Colors.END}").strip()
                
                print(f"\n{Colors.YELLOW}Select mutations (space-separated):{Colors.END}")
                print(f"  capitalize reverse leet numbers years symbols double common")
                
                mut_input = input(f"{Colors.CYAN}Mutations (or press Enter for all): {Colors.END}").strip()
                
                if mut_input:
                    mutations = mut_input.split()
                else:
                    mutations = ['capitalize', 'reverse', 'leet', 'numbers', 'years', 'symbols', 'double', 'common']
                
                print(f"{Colors.GREEN}✓ Using mutations: {', '.join(mutations)}{Colors.END}")
                result = self.hybrid_attack(wordlist, mutations)
                
            else:
                print(f"{Colors.RED}✗ Invalid choice!{Colors.END}")
                continue
            
            self.print_result(result)

if __name__ == "__main__":
    try:
        cracker = HashCracker()
        cracker.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Operation cancelled by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal error: {e}{Colors.END}")
        sys.exit(1)