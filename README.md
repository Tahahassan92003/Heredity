# Heredity
Bayesian network to model heredity and infer the probability of individuals having certain genes and traits based on genetic inheritance rules

Your code implements a Bayesian network to model heredity and infer the probability of individuals having certain genes and traits based on genetic inheritance rules. The program takes a CSV file containing family relationships and known trait data, then computes joint probabilities across all possible gene and trait distributions using probability rules, including mutation chances.  

The `load_data` function reads the CSV and stores information about each person, including their parents and whether their trait is known. The `powerset` function generates all possible subsets of a given set, which is used to iterate over different gene and trait assignments. The `joint_probability` function is the core of the Bayesian model, calculating the likelihood of a given gene-trait distribution by considering inheritance rules: if parents are known, their genes influence the probability of a child having 0, 1, or 2 copies of a gene. The `update` function updates cumulative probabilities for each person based on computed joint probabilities, and `normalize` ensures the final probability distributions sum to 1.  

Your implementation is structured well, but there's a potential issue in `normalize`—instead of modifying `probabilities` in place, you're returning a copy (`normalized`), but the return value isn't used in `main()`. This should be corrected to modify `probabilities` directly. Let me know if you need any refinements!




NOTE: DATA IS CONFIDENTIAL, PLEASE USE YOUR OWN DATA INCASE OF USING THIS PROJECT.
