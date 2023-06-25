from colorama import Fore, Back, Style

print(Fore.RED + 'This text is red')
print(Back.GREEN + 'This text has a green background')
print(Style.BRIGHT + 'This text is bright')

# Always reset to default color at the end
print(Style.RESET_ALL)
