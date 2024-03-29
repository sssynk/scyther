# Scyther Account Generator POC

Thanks to @freakyscientist for help with the second authentication part.

This is a **simple proof of concept** for a PTC account generator. It is provided in a way that other projects can build off of, but **not intended to be used as is**. This project is for educational purposes only.

## How does it work?

3 Parts (I could have made it 2 but I am keeping it as is for now)

1. Account Generator/Validator - This script generates accounts and validates them by verifying the email address via a code.
2. Code Server - This script acts as a proxy server and holds all available codes. It will send a list of all codes to the generator when requested.
3. Email Server - This script acts as a email server and receives emails and sends them to the code server.

## Setup (probably will not work)

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Make a file called proxies.txt with a list of proxies in the format `ip:port` (one per line)
4. On line 104 of `scyther_generate_sync_inf.py` change the `browser_executable_path` to the path of your browser executable (chrome) or just remove it and also in file `scyther_generate.py`
5. Set the challenge (get it from the pogo app) and email_domain variables on the 3rd line of both `scyther_generate.py` and `scyther_generate_sync_inf.py`
6. Set line 14 of scyther_email to the hook for where to send codes (could use localhost:8090 if your email server and generator are on the same machine)
7. yay you're done

## Usage (probably will not work)

1. Make sure your email server is set up and run `python scyther_email.py`
2. Make sure your code server is set up and run `python scyther_server.py`
3. Run the script with `python scyther_distributor.py` (most reliable) or `python scyther_generate_sync.py` (less reliable)
4. The script will generate accounts and save them to `accounts.txt`
