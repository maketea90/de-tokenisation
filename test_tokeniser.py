from tokeniser import Tokeniser

def test_tokeniser_splits_words():
    t = Tokeniser()
    sentence = 'hello my name is joe'
    words = ['hello', 'my', 'name', 'is', 'joe']
    assert t.tokenise(sentence) == words

def test_tokeniser_replaces_punctuation():

    t = Tokeniser()
    sentence = 'hello!!, my? NaMe... ,,, iS () Joe.'
    words = ['hello', 'my', 'name', 'is', 'joe']
    assert t.tokenise(sentence) == words

def test_tokeniser_counts_tokens():
    t = Tokeniser()
    sentence = 'hello hello hello my name is joe joe hello, s..sdf.asd?SDF'
    words = t.tokenise(sentence)
    print(words)
    token_count = t.count_tokens(words)
    assert token_count['hello'] == 4
    assert token_count['my'] == 1
    assert token_count['joe'] == 2
    assert token_count['sdf'] == 2
    assert len(token_count) == 8

def test_sort_vocab_orders_by_token_frequency():
    t = Tokeniser()
    sentence = 'hello hello hello my my name'
    words = t.tokenise(sentence)
    token_count = t.count_tokens(words)
    vocab = t.sort_vocab(token_count)
    assert vocab == [('hello', 3), ('my', 2), ('name', 1)]

def test_split_into_subwords_creates_list_of_subwords():
    t = Tokeniser()
    result = t.split_into_subwords(["cat"])
    assert result == [["c", "a", "t", t.END_OF_WORD_SYMBOL]]
    another = t.split_into_subwords(["the", "hat"])
# should return:
    assert another == [["t", "h", "e", "</w>"], ["h", "a", "t", "</w>"]]

def test_count_symbol_pairs_returns_expected_pair_frequencies():
    t = Tokeniser()
    subwords = [
        ["c", "a", "t", "</w>"],
        ["c", "a", "r", "</w>"]
    ]
    result = t.count_symbol_pairs(subwords)
    print(result)
    assert result[("c", "a")] == 2
    assert result[("a", "t")] == 1
    assert result[("a", "r")] == 1
    
def test_merge_most_frequent_pair_merges_correctly():
    t = Tokeniser()
    subwords = [
        ["t", "h", "e", "</w>"],
        ["h", "a", "t", "</w>"]
    ]
    pair_counts = {
        ("t", "h"): 1,
        ("h", "e"): 1,
        ("e", "</w>"): 1,
        ("h", "a"): 1,
        ("a", "t"): 1,
        ("t", "</w>"): 1
    }

    merged = t.merge_most_frequent_pair(subwords, pair_counts)
    print(merged)
    assert merged[0] == ["th", "e", "</w>"]
    assert merged[1] == ["h", "a", "t", "</w>"]

def test_build_bpe_vocab_merges_common_pairs_first():
    t = Tokeniser()
    tokens = ["aa", "ab", "aa"]

    merged = t.build_bpe_vocab(tokens, num_merges=1)

    expected = [
        ["aa", "</w>"],  # "aa"
        ["a", "b", "</w>"],  # "ab"
        ["aa", "</w>"]  # "aa"
    ]

    assert merged == expected

def test_build_bpe_vocab_multiple_merges():
    t = Tokeniser()
    tokens = ["aa", "ab", "aa"]
   
    result = t.build_bpe_vocab(tokens, num_merges=2)

    expected = [
        ["aa", "</w>"],  
        ["ab", "</w>"],  
        ["aa", "</w>"]   
    ]
    print(result)

    assert result == expected