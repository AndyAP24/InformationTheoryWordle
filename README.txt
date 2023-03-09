A README plaintext file that explains how your program selects the distribution π
when there are multiple words with the same minimum value for α_g (see Task 6).

Because we keep track of the min as we loop through the words, we simply choose
the first word in the order that they appear in the file or our pruned dictionary.
This is valid since as stated in task 6, if multiple words have the same min alpha,
any can be chosen.