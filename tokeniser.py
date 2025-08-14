import string
import re

class Tokeniser:

    

    def __init__(self):
        self.END_OF_WORD_SYMBOL = '</w>'
        

    def tokenise(self, text: str) -> list[str]:
        # re.sub(r'(.,!\(\)\?)+')
        # re.sub(r'()')
        
        p = string.punctuation

        regex = re.compile('[%s]' % re.escape(string.punctuation))
        out = regex.sub(' ', text)
# out = 'This is  fortunately  A Test  string'
        words = out.lower().split()
        return words

    def count_tokens(self, tokens: list[str]) -> dict[str, int]:
        token_count = {}
        for token in tokens:
            if token in token_count.keys():
                token_count[token] += 1
            else:
                token_count[token] = 1
        return token_count
    
    def sort_vocab(self, token_counts: dict[str, int]) -> list[tuple[str, int]]:
        return sorted(token_counts.items(), key=lambda x: x[1], reverse=True)

    def split_into_subwords(self, tokens: list[str]) -> list[list[str]]:
        subwords = []
        for token in tokens:
            chars = list(token)
            chars.append(self.END_OF_WORD_SYMBOL)
            subwords.append(chars)
        return subwords
    
    def count_symbol_pairs(self, subword_tokens: list[list[str]]) -> dict[tuple[str, str], int]:
        result = {}
        for subword in subword_tokens:
            for i in range(len(subword) - 1):
                # pair = subword[i] + subword[i+1]
                tuple = (subword[i], subword[i+1])
                if tuple not in result:

                    result[tuple] = 1
                else:
                    result[tuple] += 1
        return result

    def merge_most_frequent_pair(
    self,
    subword_tokens: list[list[str]],
    pair_counts: dict[tuple[str, str], int]		
) -> list[list[str]]:
        sorted_pairs = self.sort_vocab(pair_counts)
        a,b = sorted_pairs[0][0]
        result = []
        for subword in subword_tokens:
            new_subword = []
            i = 0
            while i < len(subword):
                
                if subword[i] == a and subword[i+1] == b and a != '</w>' and b != '</w>':
                    new_subword.append(a + b)
                    i += 2
                else:
                    new_subword.append(subword[i])
                    i += 1
            result.append(new_subword)
        return result
        
    def build_bpe_vocab_test(
    self,
    tokens: list[str],
    num_merges: int
) -> list[list[str]]:
        
        
        
        subwords = self.split_into_subwords(tokens)

        symbol_pair_frequencies = self.count_symbol_pairs(subwords)
        
        for i in range(num_merges):
            if i == 0:
                print(symbol_pair_frequencies)
                merged = self.merge_most_frequent_pair(subwords, symbol_pair_frequencies)
                (k := next(iter(symbol_pair_frequencies)), symbol_pair_frequencies.pop(k))
                print(symbol_pair_frequencies)
            else:
                merged = self.merge_most_frequent_pair(merged, symbol_pair_frequencies)
                (k := next(iter(symbol_pair_frequencies)), symbol_pair_frequencies.pop(k))
                print(symbol_pair_frequencies)
        return merged
    
    def build_bpe_vocab(
        self,
        tokens: list[str],
        num_merges: int
    ) -> list[list[str]]:
        # 1) words -> subwords (characters + </w>)
        subwords = self.split_into_subwords(tokens)

        # 2) apply N merges
        for _ in range(num_merges):
            pair_counts = self.count_symbol_pairs(subwords)
            # for key, value in pair_counts.items():

            # if not pair_counts:
            #     break

            merged = self.merge_most_frequent_pair(subwords, pair_counts)

            # if no changes occurred, stop (prevents infinite loop)
            if merged == subwords:
                break

            subwords = merged

        return subwords

        
            