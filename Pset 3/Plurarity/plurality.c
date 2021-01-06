#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");
        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO check if the name is in the array
    for (int i = 0; i < candidate_count; i++)
    {
        // compare two string length
        if (strlen(name) != strlen(candidates[i].name))
        {
            continue;
        }
        else
        {
            // check if each character of 2 strings matches
            bool flag = true;
            for (int j = 0; j < strlen(name); j++)
            {
                if (name[j] != candidates[i].name[j])
                {
                    flag = false;
                    break;
                }
            }
            // if they match then increment the vote of candidates[i].name
            if (flag)
            {
                candidates[i].votes++;
                return true;
            }
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    int max = 0;
    for (int i = 1; i < candidate_count; i++)
    {
        if (candidates[max].votes < candidates[i].votes)
        {
            // save the index of the maxium votes of all the candidates
            max = i;
        }
    }
    // check if there are any multiple winners.
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[max].votes == candidates[i].votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
    return;
}

