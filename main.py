from helpers import ngrams

if __name__ == '__main__':
    generator = ngrams.NgramGenerator()
    with open('Generators/Ngrams/1880/X1913RQNB5G0-maj.txt', 'r') as txt:
        generator.generate(txt.read())
