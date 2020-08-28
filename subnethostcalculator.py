import math


def getIPclass(ip_str):
    first_byte = int(ip_str.split(".")[0])
    if first_byte < 128:
        return ['255', 24]
    elif first_byte < 192:
        return ['255.255', 16]
    else:
        return ['255.255.255', 8]


def calculate_borrow_bits(custom_host_bit_len, class_host_bit_len):
    borrowed_bit_len = class_host_bit_len - custom_host_bit_len
    borrowed = ""
    for bit in range(0, borrowed_bit_len, 1):
        borrowed = borrowed + '1'
    borrowed_bit_whole_count = borrowed_bit_len // 8
    host_bit_whole_count = custom_host_bit_len // 8
    non_whole_borrowed_bit = borrowed[-1 * len(borrowed) + borrowed_bit_whole_count * 8:]
    print("Borrowed bit whole count: ", borrowed_bit_whole_count)
    print("Host bit whole count: ", host_bit_whole_count)
    print("Borrowed bit non-whole: ", non_whole_borrowed_bit)
    return [borrowed_bit_whole_count, host_bit_whole_count, non_whole_borrowed_bit]


def calculate_borrow_dec(borrowed_bit_whole_count, host_bit_whole_count, non_whole_borrowed_bit):
    borrowed_str = ''
    for i in range(0, borrowed_bit_whole_count):
        borrowed_str = borrowed_str + ".255"
    if non_whole_borrowed_bit != '11111111':
        borrowed_str = borrowed_str + "." + str(convert(non_whole_borrowed_bit))
    for i in range(0, host_bit_whole_count):
        borrowed_str = borrowed_str + ".0"
    return borrowed_str


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
    ip = input("Enter IP address (Ex: 192.168.100.0/25): ")
    ip = ip.split("/")
    ip_class_info = getIPclass(ip[0])
    borrowed_bits_info = calculate_borrow_bits(32 - int(ip[1]), ip_class_info[1])
    subnet_mask = ip_class_info[0] + calculate_borrow_dec(borrowed_bits_info[0], borrowed_bits_info[1], borrowed_bits_info[2])
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
    calculate_address(ip[0], subnet_mask, subnet_host_list)


if __name__ == '__main__':
    main()