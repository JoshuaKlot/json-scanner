import json
import re
import sys
import os

class JSONConverter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def consume(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token
        else:
            raise SyntaxError("Unexpected end of input")

    def parse(self):
        sentence = self.parse_sentence()
        return json.dumps(sentence, separators=(',', ':'))

    def parse_sentence(self):
        sentence = {"%k": "list", "%v": []}
        while self.index < len(self.tokens):
            data_literal = self.parse_data_literal()
            sentence["%v"].append(data_literal)
        return sentence

    def parse_data_literal(self):
        token = self.consume()
        if token.startswith("["):
            return self.parse_list_literal()
        elif token == "{":
            return self.parse_tuple_literal()
        elif token == "%{":
            return self.parse_map_literal()
        elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()) or token.startswith(":") or token in ["true", "false"]:
            return self.parse_primitive_literal(token)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_list_literal(self):
        list_literal = {"%k": "list", "%v": []}
        while self.tokens[self.index] != "]":
            data_literal = self.parse_data_literal()
            list_literal["%v"].append(data_literal)
            if self.tokens[self.index] == ",":
                self.consume()
        self.consume()  # Consume the closing ']'
        return list_literal

    def parse_tuple_literal(self):
        tuple_literal = {"%k": "tuple", "%v": []}
        while self.tokens[self.index] != "}":
            data_literal = self.parse_data_literal()
            tuple_literal["%v"].append(data_literal)
            if self.tokens[self.index] == ",":
                self.consume()
        self.consume()  # Consume the closing '}'
        return tuple_literal

    def parse_map_literal(self):
        map_literal = {"%k": "map", "%v": []}
        while self.tokens[self.index] != "}":
            key_pair = self.parse_key_pair()
            map_literal["%v"].append(key_pair)
            if self.tokens[self.index] == ",":
                self.consume()
        self.consume()  # Consume the closing '}'
        return map_literal

    def parse_key_pair(self):
        key = self.parse_data_literal()
        if self.tokens[self.index] == "=>":
            self.consume()
            value = self.parse_data_literal()
        else:
            value = self.parse_data_literal()
        return [key, value]

    def parse_primitive_literal(self, token):
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            return self.parse_int(token)
        elif token.startswith(":"):
            return self.parse_atom(token)
        elif token in ["true", "false"]:
            return self.parse_bool(token)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_int(self, token):
        return {"%k": "int", "%v": int(token)}

    def parse_atom(self, token):
        return {"%k": "atom", "%v": token}

    def parse_bool(self, token):
        return {"%k": "bool", "%v": True if token == "true" else False}

def main():
    print(os.getcwd())
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.txt", file=sys.stderr)
        sys.exit(1)

    input_file_path = sys.argv[1]

    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
            input_text = re.sub(r'#.*$', '', input_text, flags=re.MULTILINE)  # Remove comments
            input_text = re.sub(r'\s', '', input_text)  # Remove whitespace
            tokens = re.findall(r'\S+|:|,|\[|\]|\{|\}|%{|%}|=>|\n', input_text)  # Tokenize
            converter = JSONConverter(tokens)
            output_json = converter.parse()
            print(output_json)
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
