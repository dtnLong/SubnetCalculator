# import itertools
#
#
# def solution(l):
#     # Your code here
#     for number_length in range(len(l), 0, -1):
#         new_list = list(itertools.combinations(l, number_length))
#         biggest_result = []
#         for number_combination in new_list:
#             number_combination = sorted(number_combination, reverse=True)
#             code = ''
#             for number in number_combination:
#                 code = code + str(number)
#             code = int(code)
#             biggest_result.append(code)
#         biggest_result = sorted(biggest_result, reverse=True)
#         for code in biggest_result:
#             if code % 3 == 0:
#                 return code
#         # for list_index in range(len(new_list) - 1, -1, -1):
#         #     number_combination = new_list[list_index]
#         #     number_combination = sorted(number_combination, reverse=True)
#         #     print(number_combination)
#         #     code = ''
#         #     for number in number_combination:
#         #         code = code + str(number)
#         #     code = int(code)
#             # if code % 3 == 0:
#             #     return code
#     return 0
#
#
# print(solution([1, 0, 0, 9, 2, 3]))