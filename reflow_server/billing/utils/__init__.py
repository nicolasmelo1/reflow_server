def validate_cnpj(cnpj):
    """
    The algorithm in Brazil actually doesn't change very often. But instead of using
    an external lib we created our own CNPJ validator.
    Reference: https://www.devmedia.com.br/validando-o-cnpj-em-uma-aplicacao-java/22374

    Args:
        cnpj (str): This is a string representing the cnpj, can contain numbers, `.`, `-` or `/` characters

    Returns:
        bool: Returns True or False if the CNPJ is valid or not, respectively.
    """
    if type(cnpj) == str:
        cnpj = cnpj.replace('.','').replace('-','').replace('/','')
    
        if len(cnpj) != 14:
            return False
        
        digits = cnpj[:-2]
        dv = 11
        while len(digits) < 14:
            multiply_index = 2
            soma = 0
            for digit in digits[::-1]:
                soma += int(digit)*multiply_index
                if multiply_index < 9:
                    multiply_index += 1
                else:
                    multiply_index = 2
            validation_digit = soma % dv

            if validation_digit > 1:
                digits += str(dv - validation_digit)
            else:             
                digits += str(0)
        return digits == cnpj
    else:
        return False

def validate_cpf(cpf):
    """
    The algorithm in Brazil actually doesn't change very often. But instead of using
    an external lib we created our own CPF validator.
    Reference: https://www.devmedia.com.br/validar-cpf-com-javascript/23916

    Args:
        cpf (str): This is a string representing the cpf, can contain numbers, `.`, `-` or `/` characters

    Returns:
        bool: Returns True or False if the CNPJ is valid or not, respectively.
    """
    if type(cpf) == str:
        cpf = cpf.replace('.','').replace('-','').replace('/','')

        if len(cpf) != 11:
            return False

        digits = cpf[:-2]
        multiplier = 10
        divisor = 11
        while len(digits) < 11:
            soma = 0
            for index, digit in enumerate(digits):
                soma += int(digit) * (len(digits) + 1 - index)
            remainder = (soma * multiplier) % divisor
            remainder = remainder if remainder not in [multiplier, divisor] else 0
            digits += str(remainder)
        return digits == cpf
    else:
        return False

