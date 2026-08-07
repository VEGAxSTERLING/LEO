![image alt](https://github.com/VEGAxSTERLING/LEO/blob/31e926d37ec080ee57b004b49da77b2eedff2efa/Banner.jpg)
===========================================================================================================
<div align="center">

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-Educational-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/status-Active-success.svg)

**Password Recovery & Security Testing Tool**

*by VEGAxSTERLING | Ethical Hacking & Cybersecurity*

</div>

---

## Overview

LEO is a high-performance password recovery tool designed for ethical penetration testing and security research. Features 27 hash algorithms, multi-core processing, and intelligent attack strategies for authorized security assessments.

### Key Features

* **Multi-Core Processing** - Automatic CPU optimization
* **27 Hash Algorithms** - MD5, SHA family, BLAKE2, NTLM, and more
* **3 Attack Methods** - Dictionary, Brute-force, Hybrid
* **Real-Time Stats** - Live hash rate and progress monitoring
* **Professional Grade** - Built for real-world pentesting

---

## Quick Start

```bash
# Installation
git clone https://github.com/VEGAxSTERLING/LEO.git
cd LEO

# Optional dependencies
pip install pycryptodome bcrypt argon2-cffi

# Run
python3 LEO.py
```

---

## Usage

### Basic Workflow

1. Launch tool and enable multi-core processing
2. Select attack method (Dictionary/Brute-force/Hybrid)
3. Choose hash algorithm (1-27)
4. Enter target hash
5. Configure attack parameters

### Example: Dictionary Attack

```bash
Select attack method: 1
Select algorithm (1-27): 1  # MD5
Enter target hash: 5f4dcc3b5aa765d61d8327deb882cf99
Enter wordlist path: rockyou.txt
```

---

## Supported Algorithms (27 Total)


| Category        | Algorithms                                |
| --------------- | ----------------------------------------- |
| **Classic**     | MD5, SHA1, SHA224, SHA256, SHA384, SHA512 |
| **SHA-3**       | SHA3-224, SHA3-256, SHA3-384, SHA3-512    |
| **Modern**      | BLAKE2b, BLAKE2s, SHAKE-128, SHAKE-256    |
| **Specialized** | RIPEMD-160, Whirlpool, SM3                |
| **Windows**     | NTLM, LM Hash                             |
| **Database**    | MySQL (SHA1), MD4                         |
| **Encoded**     | MD5/SHA256 (Base64)                       |
| **Double**      | MD5(MD5), SHA1(SHA1)                      |
| **Salted**      | MD5(pass:salt), SHA256(salt:pass)         |

---

## Attack Methods

### 1. Dictionary Attack

Fast wordlist-based cracking with multi-core support. Best for common passwords.

**Usage**: Provide wordlist path (e.g., rockyou.txt)

### 2. Brute-Force Attack

Comprehensive character combination testing. Best for short passwords.

**Options**:

* Length range (1-4 recommended for speed)
* Character sets: lowercase, uppercase, digits, alphanumeric, symbols

### 3. Hybrid Attack

Intelligent mutations combining wordlist + transformations.

**Mutations**: capitalize, reverse, leet speak, numbers, years, symbols, doubles, common patterns

---

## Performance


| Algorithm | Hash Rate\* | Use Case       |
| --------- | ----------- | -------------- |
| MD5       | 1M+ h/s     | Legacy systems |
| SHA1      | 800K+ h/s   | Git, legacy    |
| SHA256    | 400K+ h/s   | Modern systems |
| NTLM      | 900K+ h/s   | Windows auth   |

\*Approximate rates - varies by CPU/cores

### Optimization Tips

* Enable multi-core processing (always)
* Use SSD for wordlist storage
* Choose faster algorithms when possible
* Remove duplicate wordlist entries

---

## Legal & Ethical Use

### Authorization Required

**This tool is for AUTHORIZED security testing ONLY.**

✅ **Permitted Uses:**

* Penetration testing with written authorization
* Security research and education
* Password strength assessment
* Incident response and forensics

❌ **Prohibited:**

* Unauthorized system access
* Malicious activities
* Testing without explicit permission

### Disclaimer

**Unauthorized access to computer systems is illegal.** The author is NOT responsible for misuse. Always obtain proper authorization and comply with all applicable laws.

---

## Contributing

Contributions welcome! Submit issues and pull requests on GitHub.

### Guidelines

* Follow PEP 8 standards
* Test thoroughly
* Update documentation
* Consider security implications

---

## Author

**Vega Sterling**

- Cybersecurity Researcher | Pentester | Open-Source Developer
- Security Content Creator (Linkedin, Medium, Quora)
- Mission: Spreading cybersecurity awareness through education

### Connect with me:

- Linkedin: [@VEGA STERLING](https://www.linkedin.com/in/vega-sterling-a91163343/)
- Quora: [@VEGA STERLING](https://www.quora.com/profile/Vega-Sterling-2)
- Medium: [@VEGA STERLING](https://vega-sterling.medium.com/)

---

## License

Educational Use License - For authorized security testing only.

```
Copyright (c) 2025 VEGAxSTERLING
Provided "AS IS" without warranty.
Unauthorized use is prohibited.
```

---

*Stay ethical. Stay safe. Stay curious.*

⭐ Star if you find this useful!

</div>