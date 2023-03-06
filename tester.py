import wordlesolver

def test_pattern_gen():
    pattern = wordlesolver.generate_pattern("array", "tasks")
    assert pattern == "YBBBB", f"Generated {pattern} instead of YBBBB"
    pattern = wordlesolver.generate_pattern("aarva", "array")
    assert pattern == "GYGBB", f"Generated {pattern} instead of GYGBB"


if __name__ == "__main__":
    test_pattern_gen()