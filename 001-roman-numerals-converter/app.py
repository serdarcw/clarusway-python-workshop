from flask import Flask, render_template, request

app = Flask(__name__)

def roman_converter(n):   
    symbols = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), 
               (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), 
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]    
    roman_number = ''
    for num, letter in symbols:
        roman_number += letter * (n//num)
        n %= num
    return roman_number

@app.route('/', methods = ['GET'])
def main_get():
    return render_template('index.html', developer_name = 'Talha', not_valid = False)

@app.route('/', methods = ['POST'])
def main_post():
    alpha = request.form['number']
    if not alpha.isdecimal():
        return render_template('index.html', developer_name = 'Talha', not_valid = True)
    number = int(alpha)
    if not 0 < number < 4000:
        return render_template('index.html', developer_name = 'Talha', not_valid = True)
    return render_template('result.html', number_decimal = number, number_roman = roman_converter(number), developer_name = 'Talha')

if __name__ == '__main__':
    app.run('0.0.0.0', port = 80)