import wordlesolver

def test_pattern_gen():
    pattern = wordlesolver.generate_pattern("array", "tasks")
    assert pattern == "YBBBB", f"Generated {pattern} instead of YBBBB"
    pattern = wordlesolver.generate_pattern("aarva", "array")
    assert pattern == "GYGBB", f"Generated {pattern} instead of GYGBB"

def test_pattern_check():
    pattern = wordlesolver.generate_pattern("array", "tasks")
    print(pattern)
    assert "tasks" in wordlesolver.filter_words(pattern, "array"), "Pattern check not working, case 1."
    assert "tasks" not in wordlesolver.filter_words(pattern, "krane"), "Pattern check not working, case 2."

if __name__ == "__main__":
    test_pattern_gen()
    test_pattern_check()
