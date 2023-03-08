import wordlesolver

def test_pattern_gen():
    pattern = wordlesolver.generate_pattern("array", "tasks")
    assert pattern == "YBBBB", f"Generated {pattern} instead of YBBBB"
    pattern = wordlesolver.generate_pattern("aarva", "array")
    assert pattern == "GYGBB", f"Generated {pattern} instead of GYGBB"

def test_pattern_check():
    pattern = wordlesolver.generate_pattern("array", "nahal")
    print(pattern)
    assert "nahal" in wordlesolver.pattern_check(pattern, "array"), "Pattern check not working, case 1."
    # assert "jails" not in wordlesolver.pattern_check(pattern, "array"), "Pattern check not working, case 2."
    print(len(wordlesolver.pattern_check(pattern, "array")))

    pattern = wordlesolver.generate_pattern("bruja", "jails")
    assert "bruja" in wordlesolver.pattern_check(pattern, "jails"), "Pattern check not working, case 3."


if __name__ == "__main__":
    test_pattern_gen()
    test_pattern_check()
