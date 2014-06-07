import re

def is_domain_valid(domain):

    if domain is None or (type(domain) is not str and type(domain) is not unicode):
        return False
    
    #first check if its a valid domain name
    
    pattern_domain = '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)\/?$'
    if re.match(pattern_domain, domain):
        return True

    
    #its not a valid domain name, may be its an IP
    pattern_ip = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not re.match(pattern_ip, domain):
        return False

    #check if its the localhost or self address
    if domain == '127.0.0.1' or domain == '10.0.0.1':
        return False                #not a valid IP


    return True


if __name__ == "__main__":

    domains = ['www.google.com', 'http://www.google.com', 'https://www.google.com',
               'google.com', 'google.io', '123.12.52.14', 'google', 'd/ab', '127.0.0.1', '10.0.0.1',
               '212.345.12.12']

    for domain in domains:
        print is_domain_valid(domain)
    
