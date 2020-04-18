from typing import Union, Literal, Tuple
import Levenshtein
import fasttext

SIMILARITY_THRESHOLD = 0.8


def is_similar_levenstein(str1: str, str2: str) -> Tuple[bool, float]:
    """[summary] TODO

    Arguments:
        str1 {str} -- [description]
        str2 {str} -- [description]
    Returns:
        Tuple[bool, float] -- [description]
    """
    ratio = Levenshtein.ratio(str1, str2)

    if ratio < SIMILARITY_THRESHOLD:
        return (False, ratio)
    else:
        return (True, ratio)


def is_similar_fasttext(str1: str, str2: str) -> Tuple[bool, float]:
    """[summary] TODO

    Arguments:
        str1 {str} -- [description]
        str2 {str} -- [description]
    Returns:
        Tuple[bool, float] -- [description]
    """
    # !!модель весит 6.7GB!!
    kaz_ft_model = fasttext.load_model(path="./models/cc.kk.300.bin")

    str1_tok = fasttext.tokenize(text=str1)
    str2_tok = fasttext.tokenize(text=str2)


    ratio = Levenshtein.ratio(str1, str2)

    if ratio < SIMILARITY_THRESHOLD:
        return (False, ratio)
    else:
        return (True, ratio)


def is_similar(
    str1: str,
    str2: str,
    method: Union[Literal["levenshtein"], Literal["fasttext"]],
) -> Tuple[bool, float]:
    """[summary] TODO

    Arguments:
        str1 {str} -- [description]
        str2 {str} -- [description]
        method {Union[Literal[} -- [description]
    Returns:
        Tuple[bool, float] -- [description] sim_score
    """
    if method == "levenshtein":
        return is_similar_levenstein(str1=str1, str2=str2)
    else:
        return (False, 0.0)


if __name__ == "__main__":
    print('str1="qwertyuiop", str2="asdfghjkl"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="asdfghjkl", method="levenshtein"),
    )
    print()
    print('str1="qwertyuiop", str2="qwerthjkl"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwerthjkl", method="levenshtein"),
    )
    print()
    print('str1="qwertyuiop", str2="qwertyuikl"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwertyuikl", method="levenshtein"),
    )
    print()
    print('str1="qwertyuiop", str2="qwertyuiop"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwertyuiop", method="levenshtein"),
    )

# str1="qwertyuiop", str2="asdfghjkl"
# similarity: (False, 0.0)

# str1="qwertyuiop", str2="qwerthjkl"
# similarity: (False, 0.5263157894736842)

# str1="qwertyuiop", str2="qwertyuikl"
# similarity: (True, 0.8)

# str1="qwertyuiop", str2="qwertyuiop"
# similarity: (True, 1.0)
