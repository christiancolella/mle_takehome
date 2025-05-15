def print_color(str, color):
  '''
  Prints the given string to the console with the desired color.
  
  Parameters
  ----------
  str: str - The string to be printed.
  color: str - The choice of color. Options:
    'gray', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    
  Returns
  -------
  nothing
  '''
  
  if color == 'gray':
    print('\033[1;90m' + str + '\033[0m')
    return
    
  if color == 'red':
    print('\033[1;91m' + str + '\033[0m')
    return
  
  if color == 'green':
    print('\033[1;92m' + str + '\033[0m')
    return
    
  if color == 'yellow':
    print('\033[1;93m' + str + '\033[0m')
    return
    
  if color == 'blue':
    print('\033[1;94m' + str + '\033[0m')
    return
  
  if color == 'magenta':
    print('\033[1;95m' + str + '\033[0m')
    return
    
  if color == 'cyan':
    print('\033[1;96m' + str + '\033[0m')
    return
    
  if color == 'white':
    print('\033[1;97m' + str + '\033[0m')
    return
  
  # Invalid color
  raise ValueError(f'Invalid color \'{color}\'')
