import random
import sys
from difflib import SequenceMatcher
from math import ceil

'अंग्रेजा', 'पड़ते', 'बनीं',

skip_tokens = ('गे', 'दे', 'ले', 'गा','जाए','जा', 'ला', 'ले', 'पा', 'खा', 'चाहिए', 'समाजवादी', 'विधानसभा', 'थालिपीठे', 'मराठवाड़ा', 'अन्यथा', 'खुफिया', 'अनसुना', 'इन्होंने')
exceptions = (('है', 'हैं'), ('था', 'थे', 'थी', 'थीं'), ('हुआ', 'हुई', 'हुए', 'हुईं'))
conjugated_adj = ('लंबा', 'ऊंचा', 'धीमा', 'महंगा', 'गीला', 'भूरा', 'मोटा', 'हल्का', 'पुराना',
                  'ताज़ा', 'बुरा', 'फिस्लाहा', 'कड़वा', 'चौड़ा', 'चौड़ा', 'सुखा', 'नमा', 'खट्टा', 'पतला', 'लम्बा', 'अच्छा', 'हरा', 'थोड़ा',
                  'बड़ा', 'बूढा', 'कड़वा', 'निचा', 'चमकीला', 'मीठा', 'पीला', 'भोला', 'गाढ़ा', 'खुरदुरा', 'ठंडा', 'गंदा', 'तीता', 'सस्ता',
                  'छोटा', 'नया', 'गीरा', 'सूखा', 'गहरा', 'सीधा', 'खारा', 'दुबला', 'चिपचिपा',
                  'नीला','तीखा','डरावना','सुनहरा','इकलौता','तीखा','समूचा','पुरा','अनूठा', 'सुरीला',
                  'ख़रीदा','संकरा','रूखा','अंधा','बहरा','बौना','ठिगना','पैना','घना','डरावना',
                  'अनूठा','झूठा','इकट्ठा','भरा','अधूरा', 'नुकीला','उबला','ढीला','पक्का',
                  'पहला', 'दूसरा','तीसरा','चौथा','पांचवा','छठा','पचवा','सातवा','आठवा',
                  'नौवा', 'दसवा' ,
                  )

adj = ('ा', 'े', 'ी')
vb = ('ा', 'े', 'ी', 'ीं')

endings1 = ('या', 'ए', 'ई', 'ईं',)
endings2 = ('या', 'ये', 'यी', 'यीं')



def convert_to_edits(err, cor):
    return f'{err}\n{cor}\n'


def convert_to_wdiff(err, cor):
    result = []
    err_toks, cor_toks = err.split(), cor.split()
    matcher = SequenceMatcher(None, err_toks, cor_toks)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        err_part = ' '.join(err_toks[i1:i2])
        cor_part = ' '.join(cor_toks[j1:j2])
        if tag == 'replace':
            result.append("[-{}-] {{+{}+}}".format(err_part, cor_part))
        elif tag == 'insert':
            result.append("{{+{}+}}".format(cor_part))
        elif tag == 'delete':
            result.append("[-{}-]".format(err_part))
        else:
            result.append(err_part)
    return ' '.join(result)


def sentence_wise(file):
    sentence = []
    for line in file:
        line = line.strip()
        if line == '</s>':
            yield sentence
            sentence = []
        elif line == '<s>':
            pass
        else:
            sentence.append(line)
    yield sentence


def pos_tag(sentence):
    actual_words = []
    tags = []
    tags_better = []
    for word in sentence:
        components = word.split('\t')
        actual_words.append(components[0])
        tags.append(components[2])
        tags_better.append(components)
    return zip(actual_words, tags, tags_better)


def random_except(options, choice):
    remaining = list(options)
    remaining.remove(choice)
    return random.choice(remaining)


def endswith_any(word, endings):
    for ending in endings:
        if word.endswith(ending):
            return ending


def insert_errors(pos_tags):
    err = []
    cor = []

    for token, tag, _ in pos_tags:
        try:
            if token in skip_tokens or len(token) < 2:
                err.append(token)
            elif tag == 'PSP' and token[-1] in adj and token[-2] in ('क', 'ल'):
                err.append(token[:-1] + random_except(adj, token[-1]))
            elif list(filter(lambda ex: token in ex, exceptions)):
                exs = list(filter(lambda ex: token in ex, exceptions))
                err.append(random_except(exs[0], token))
            elif len(token) >4 and token[-1] in adj and  token[-4:-1] == 'वाल':
                err.append(token[:-1] + random_except(adj, token[-1]))
            elif tag in ('JJ', 'QO') and token[-1] in adj and (token[:-1] + adj[0]) in conjugated_adj:
                err.append(token[:-1] + random_except(adj, token[-1]))
            elif tag == 'PRP' and token[-1] in adj and (token[-2] in ('र', 'क') or token.startswith('अप')):
                err.append(token[:-1] + random_except(adj, token[-1]))
            elif tag == 'VAUX':
                if len(token) == 2 and token[-1] in vb[-2:]:
                    err.append(token[0] + random.choice(endings1[:2]))
                elif endswith_any(token, endings1):
                    ending = endswith_any(token, endings1)
                    substitute = random_except(endings1, ending)
                    if token[:len(ending)][-1] == 'ि' and substitute in ('ई', 'ईं'):
                        err.append(token[:-3] + random.choice(vb[-2:]))
                    else:
                        err.append(token.strip(ending) + substitute)
                elif endswith_any(token, endings2):
                    ending = endswith_any(token, endings2)
                    err.append(token[:-len(ending)] + random_except(endings2, ending))
                elif token[-1] in vb:
                    err.append(token[:-1] + random_except(vb, token[-1]))
                else:
                    err.append(token)
            elif tag == 'VM' and token[-1] in adj:
                if len(token) == 2 and token[-1] in vb[-2:]:
                    err.append(token[0] + random.choice(endings1[:2]))
                elif token[-2] == 'न' and token[-1] in ('ा', 'े'):
                    err.append(token[:-1] + random_except(('ा', 'े'), token[-1]))
                elif token[-2] == 'ग':
                    substitute = random_except(adj, token[-1])
                    if token[-3] == 'ं':  # karenge -> karega:
                        token = token[:-3] + token[-2:]
                    elif substitute == 'े':
                        token = token[:-2] + 'ं' + token[-2:]
                    err.append(token[:-1] + substitute)
                elif endswith_any(token, endings1):
                    ending = endswith_any(token, endings1)
                    substitute = random_except(endings1, ending)
                    if token[:len(ending)][-1] == 'ि' and substitute in ('ई', 'ईं'):
                        err.append(token[:-3] + random.choice(vb[-2:]))
                    else:
                        err.append(token.strip(ending) + substitute)
                elif endswith_any(token, endings2):
                    ending = endswith_any(token, endings2)
                    err.append(token[:-len(ending)] + random_except(endings2, ending))
                else:
                    substitute = random_except(adj, token[-1])
                    err.append(token[:-1] + substitute)
            else:
                err.append(token)
            cor.append(token)
        except IndexError as e:
            print(token, tag, e, file=sys.stderr)
    return ' '.join(err), ' '.join(cor)


def select_edits(err, cor, selection_ratio=1):
    mismatch = []
    err, cor = err.split(), cor.split()
    mm = []
    for i, (er, co) in enumerate(zip(err, cor)):
        if er != co:
            mm.append((er, co))
            mismatch.append(i)
    num_edits = ceil(len(mismatch) * selection_ratio)
    for i in sorted(random.sample(mismatch, num_edits)):
        cor_cpy = cor[:]
        cor_cpy[i] = err[i]
        yield ' '.join(cor), ' '.join(cor_cpy)


def main(args):
    with open(args.input_file) as input_file:
        for sentence in sentence_wise(input_file):
            sentence_tagged = pos_tag(sentence)
            inserted_errors = insert_errors(sentence_tagged)
            if args.single is not None:
                inserted_errors = select_edits(*inserted_errors, args.single)
            else:
                inserted_errors = [inserted_errors]
            for cor, err in inserted_errors:
                if args.edits:
                    print(convert_to_edits(err, cor))
                else:
                    print(convert_to_wdiff(err, cor))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Insert Errors into a sentence file')
    parser.add_argument('input_file', default='hindi.output', nargs='?', help='input filename')
    parser.add_argument('--single', nargs='?', const=0.6, type=int, help='format')
    parser.add_argument('--edits', action='store_true', help='format')
    parser_args = parser.parse_args()

    random.seed(1234)

    main(parser_args)
