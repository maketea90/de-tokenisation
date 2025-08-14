import string
import re

class Tokeniser:

    

    def __init__(self):
        self.END_OF_WORD_SYMBOL = '</w>'
        self.vocab: set[str] = set({})
        

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
                
                if subword[i] == a and subword[i+1] == b:
                    new_subword.append(a + b)

                    i += 2
                else:
                    new_subword.append(subword[i])
                    i += 1
            result.append(new_subword)
        return result
    
    def build_bpe_vocab(
        self,
        tokens: list[str],
        num_merges: int
    ) -> list[list[str]]:
        # 1) words -> subwords (characters + </w>)
        subwords = self.split_into_subwords(tokens)

        
        
        # pair_counts = self.count_symbol_pairs(subwords)


        # filtered_pairs = {}
        # for p, c in pair_counts.items():
        #     if p[1] != self.END_OF_WORD_SYMBOL:
        #         filtered_pairs[p] = c
        # 2) apply N merges
        # print(subwords)   
        for word in subwords:
            self.vocab.update(word)
        
        
        for _ in range(num_merges):
                
            pair_count = self.count_symbol_pairs(subwords)
            
            filtered_pairs = {}
            for p, c in pair_count.items():
                if p[1] != self.END_OF_WORD_SYMBOL:
                    filtered_pairs[p] = c
            # print(filtered_pairs)
            if filtered_pairs == {}:
                break
            merged = self.merge_most_frequent_pair(subwords, filtered_pairs)
            a, b = max(filtered_pairs.items(), key=lambda x: x[1])[0]
            print(a, b)
            self.vocab.add(a + b)
            # print(merged)
                    
            subwords = merged
        # self.vocab = set(self.vocab)
        return subwords
    
    def get_vocab(self) -> set[str]:
        return self.vocab
    


        
            