# HD-tree-based-vect-index-eval

An experimental evaluation of high-dimensional tree-based vector indexing

The full report can be found [here](Report.pdf).

KD-Tree experiments can be found in the [KD-Tree notebook](kd.ipynb).

R-Tree experiments can be found in the [R-Tree notebook](r.ipynb).

# Variants identified

## KD-Tree

**Dimension choice**

- Alternating the dimension in a cyclic way ($O(1)$)
- Randomly choosing the dimension ($O(1)$)
- Identifying the dimension of maximum variance ($O(n+d)$)
- The dimension is the one over which is longest side of the minimum-bounding-rectangle of the data ($O(d+d\times n)$)

**Split position choice**

- The median value of our datapoints across the chosen dimension ($O(1)$ if we know the length of the dataset, $O(n)$ otherwise)
- The mean value of our datapoints across the chosen dimension (sum / #datapoints) ($O(n)$ / or $O(1)$ if we already have the mean from the dimension choice when calculating the variance)
- Random value in the interval between the maximum and minimum values of our datapoints across the chosen dimension ($O(1)$)
- Geometric centre: (Maximum value + minimum value) / 2 ($O(n)$ / or $O(1)$ if we already have the maximum and minimum values from the dimension choice)

## R-Tree

Dividing the data into two groups. Starting by **choosing two seeds**:

- Choosing one random dimension over which we choose the two farthest points ($O(n)$)
- Iterating over all pairs of points and choosing the pair which has the longest distance between them ($O(n^2)$)

Then iterating over the points and **choosing to which group they will belong**:

2 choices: sacrifice clustering or sacrifice tree balancing

- Depending on the distance to the seed of the group: a point belongs to group 1 instead of group 2 if its distance to the seed of group 1 is smaller than its distance to the seed of group 2. ($O(n)$)
- Choose one of the seeds, then calculate the distance between it and the rest of the points. ($O(n)$). Sort the points, in ascending order by their previously calculated distances. Divide the points into two equal groups based on the sort. ($O(n.log(n))$)


## M-Tree

Same variants as the R-Tree with the difference in metric space:

- Euclidian space
- Manhattan space
