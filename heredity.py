import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data



def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]



def joint_probability(people, one_gene, two_genes, have_trait):
    result_probability = 1
    for individual in people:
        gene_count = 1 if individual in one_gene else 2 if individual in two_genes else 0
        has_trait = True if individual in have_trait else False
        gene_probability = PROBS['gene'][gene_count]
        trait_probability = PROBS['trait'][gene_count][has_trait]
        if people[individual]['mother'] is None:
            result_probability *= gene_probability * trait_probability
        else:
            mother = people[individual]['mother']
            father = people[individual]['father']
            parent_percentages = {}
            for parent in [mother, father]:
                gene_number = 1 if parent in one_gene else 2 if parent in two_genes else 0
                mutation_prob = 0 + PROBS['mutation'] if gene_number == 0 else 0.5 if gene_number == 1 else 1 - PROBS['mutation']
                parent_percentages[parent] = mutation_prob
            if gene_count == 0:
                result_probability *= (1 - parent_percentages[mother]) * (1 - parent_percentages[father])
            elif gene_count == 1:
                result_probability *= (1 - parent_percentages[mother]) * parent_percentages[father] + parent_percentages[mother] * (1 - parent_percentages[father])
            else:
                result_probability *= parent_percentages[mother] * parent_percentages[father]
            result_probability *= trait_probability
    return result_probability



def update(probabilities, one_gene, two_genes, have_trait, p):
    for individual in probabilities:
        gene_number = 1 if individual in one_gene else 2 if individual in two_genes else 0
        probabilities[individual]["gene"][gene_number] += p
        probabilities[individual]["trait"][individual in have_trait] += p


def normalize(probabilities):
    normalized = probabilities.copy()
    for person in probabilities:
        for typ in ['gene', 'trait']:
            total_sum = sum(probabilities[person][typ].values())
            for category in probabilities[person][typ]:
                individual_val = probabilities[person][typ][category]
                normalized_val = individual_val / total_sum
                normalized[person][typ][category] = normalized_val
    return normalized


if __name__ == "__main__":
    main()
