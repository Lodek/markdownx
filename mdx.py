#!/usr/bin/python
import subprocess, sys, re

class Parser:

    variables = {}
    txt = ''
    lines = []
    command_matches = []
    output = ''

    def __init__(self, txt):
        self.txt = txt
        self.output = txt
        
    def parse(self):
        self.read_variables()
        self.read_commands()
        self.substitute_variables()
        self.execute_commands()
        
    def read_variables(self):
        """Create dictionary with variable names and values"""
        exp = r'^\$\$([a-zA-Z_][a-zA-Z0-9_]+)=(.*)$'
        matches = list(re.finditer(exp, self.txt, flags=re.MULTILINE))
        self.variables = {match.group(1) : match.group(2) for match in matches if match}
        

    def read_commands(self):
        """Create list of commands whose output will be captured"""
        exp = r'\$\$\((.*)\)'
        self.command_matches = list(re.finditer(exp, self.txt, flags=re.MULTILINE))
        

    def substitute_variables(self):
        """Replace all occurences of the variables with the given value"""
        fmt = '$${}'
        for variable, value in self.variables.items():
            placeholder = fmt.format(variable)
            self.output = self.output.replace(placeholder, value)

    def execute_commands(self):
        """Execute commands identified and replace their output"""
        for match in self.command_matches:
            cmd = match.group(1)
            result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
            out = result.stdout.decode('utf-8')
            self.output = self.output.replace(match.group(0), out)
            
def main():
    with open(sys.argv[1], 'r') as f:
        txt = f.read()
    parser = Parser(txt)
    parser.parse()
    print(parser.output)
    

if __name__ == '__main__':
    main()
