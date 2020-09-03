import math


def convert(bin_str):
    bin_str_len = len(bin_str)
    dec_result = 0
    for i in range(0, bin_str_len, 1):
        dec_result = dec_result + (int(bin_str[i]) * pow(2, 7 - i))
    return str(dec_result)


def AND(num1, num2):
    num1 = str(bin(num1)[2:])
    num2 = str(bin(num2)[2:])
    result = ""
    for i in range(8 - len(num1)):
        num1 = '0' + num1
    for i in range(len(num1)):
        if num1[i] == '1' and num2[i] == '1':
            result = result + '1'
        else:
            result = result + '0'
    result = str(int(result, 2))
    return result


def calculate_network_address(ip_address, subnet_mask):
    network_address = ip_address.split(".")[0]
    ip_address_loc = 0
    subnet_mask_loc = 0
    for index, octet in enumerate(subnet_mask.split(".")):
        if index == 0:
            continue
        if octet == "0":
            network_address = network_address + "." + "0"
        elif subnet_mask[index] != "255":
            ip_address_loc = int(ip_address.split(".")[index])
            subnet_mask_loc = int(octet)
            network_address = network_address + "." + AND(ip_address_loc, subnet_mask_loc)
        else:
            network_address = network_address + "." + ip_address.split(".")[index]
    return network_address


def calculate_subnet_multiplier(subnet_mask):
    subnet_mask = subnet_mask.split(".")
    for i in range(len(subnet_mask)):
        if subnet_mask[i] == '0':
            return int((256 - int(subnet_mask[i - 1])) * math.pow(256, 4 - i))
    return 256 - int(subnet_mask[3])


def calculate_current_host(current_network_address):
    current_network_address = current_network_address.split(".")
    current_network_address = list(map(int, current_network_address))
    current_network_address[3] = current_network_address[3] + 1
    if current_network_address[3] > 255:
        current_network_address[3] = 0
        current_network_address[2] = current_network_address[2] + 1
        if current_network_address[2] > 255:
            current_network_address[2] = 0
            current_network_address[1] = current_network_address[1] + 1
            if current_network_address[1] > 255:
                current_network_address[1] = 0
                current_network_address[0] = current_network_address[0] + 1
    return (str(current_network_address[0]) + "." + str(current_network_address[1]) + "."
            + str(current_network_address[2]) + "." + str(current_network_address[3]))


def calculate_address(ip_address, subnet_mask, subnet_host_list):
    base_network_address = calculate_network_address(ip_address, subnet_mask)
    print("Base network address: ", base_network_address)
    base_subnet_multiplier = calculate_subnet_multiplier(subnet_mask)
    print("Base subnet multiplier: ", base_subnet_multiplier)
    # subnet_multiplier_current = int(base_network_address.split(".")[3]) + base_subnet_multiplier
    current_address = base_network_address
    for index, host in enumerate(subnet_host_list):
        # network_address = str(network_address_1) + "." + str(network_address_2) + "." + str(network_address_3) + "." + str(network_address_4)
        print("Network address of subnet", index + 1, ": ", current_address)
        current_address = calculate_current_host(current_address)
        for i in range(1, base_subnet_multiplier - 1):
            if i <= host - 2:
                print("Subnet ", index + 1, "host ", i, ": ", current_address)
            current_address = calculate_current_host(current_address)
        print("Subnet ", index + 1, "broadcast address: ", current_address)
        current_address = calculate_current_host(current_address)
        # network_address_4 = network_address_4 + (subnet_multiplier_current - network_address_4)
        # subnet_multiplier_current = subnet_multiplier_current + base_subnet_multiplier
        print()


def main():
    ip = input("Enter IP address (Ex: 192.168.100.0): ")
    subnet_mask = input("Enter subnet mask:  ")
    print("Subnet mask: ", subnet_mask)
    print()
    subnets = int(input("Enter needed subnets: "))
    subnet_host_list = []
    max_host = 0
    for i in range(1, subnets + 1, 1):
        host = int(input("Enter needed host for subnet " + str(i) + ": ")) + 2
        subnet_host_list.append(host)
        if host > max_host:
            max_host = host
    print()
    calculate_address(ip, subnet_mask, subnet_host_list)


if __name__ == '__main__':
    main()
