#include <cs50.h>
#include <stdio.h>
#include <string.h>
// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX] = {0};

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;
// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool loop_check(int start, int end, int cycle_start);
int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Check if the name is valid
    for (int i = 0; i < candidate_count; i++)
    {
        if (strlen(name) == strlen(candidates[i]))
        {
            // create a flag
            bool flag = false;
            string check_name = candidates[i];
            for (int j = 0; j < strlen(name); j++)
            {
                // if there is a diffrenece when comparing
                if (name[j] != check_name[j])
                {
                    flag = true;
                    break;
                }
            }
            // if there is not any flag raised, update the rank
            if (!flag)
            {
                ranks[rank] = i;
                return true;
            }
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    // initialize the value to 0
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // eliminate the 0 preferences
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO: sorting the pairs using selection sort
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = i + 1; j < pair_count; j++)
        {
            int pair_i = preferences[pairs[i].winner][pairs[i].loser];
            int pair_j = preferences[pairs[j].winner][pairs[j].loser];
            if (pair_i < pair_j)
            {
                // switch two addresses using a temp variable
                pair temp = pairs[i];
                pairs[i] = pairs[j];
                pairs[j] = temp;
            }
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // the first pair is locked
    for (int i = 0; i < pair_count; i++)
    {
        if (!loop_check(pairs[i].winner, pairs[i].loser, pairs[i].winner))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}
// Tests for a loop by checking for a arrow coming into a given candidate
bool loop_check(int start, int end, int cycle_start)
{
    if (end == cycle_start)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[end][i])
        {
            if (loop_check(end, i, cycle_start))
            {
                return true;
            }
        }
    }
    return false;
}
// Print the winner of the election
void print_winner(void)
{
    // winner is the index of the array candidates
    int winner = 0;
    int total_true = 0;
    // find the row index has the most true values.
    for (int i = 0; i < candidate_count; i++)
    {
        int total_true_temp = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] == true)
            {
                total_true_temp++;
            }
        }
        if (total_true_temp > total_true)
        {
            total_true = total_true_temp;
            winner = i;
        }
    }
    // print the candiate with the row index having the most true values.
    printf("%s\n", candidates[winner]);
    return;
}

