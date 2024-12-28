### 1. **KD-Tree Overview**

A KD-Tree is a data structure used for organizing points in a **k-dimensional space**. It is a binary tree where:
- Each node represents a point in the k-dimensional space.
- Each internal node corresponds to a **hyperplane** that divides the space into two subspaces, and this division continues recursively.

### 2. **Discriminant Choice**

The discriminant is the dimension (coordinate axis) along which the data is split at each node. Different strategies are used to select this dimension.

#### a) **Alternating the Discriminant in a Cyclic Way**

Let the set of dimensions be denoted as $ D = \{1, 2, \ldots, k\} $, where $ k $ is the number of dimensions in the data space. The discriminant dimension is selected by cycling through the dimensions in a fixed order. For instance, the first split is along the first dimension, the second along the second dimension, and so on. After reaching the $ k $-th dimension, the process repeats starting from the first dimension again.

Mathematically, if the current depth of the tree is $ d $, then the discriminant dimension is chosen as:
$$
\text{discriminant}_d = D[(d-1) \mod k + 1]
$$
where $ "\mod" $ is the modulo operation.

#### b) **Randomly Choosing the Discriminant (Baseline)**

In this variant, the discriminant dimension is selected randomly at each node. If there are $ k $ dimensions, the discriminant at depth $ d $ is chosen uniformly at random from $ \{1, 2, \ldots, k\} $. Let $ \text{rand}_d $ be the random dimension chosen for the split at depth $ d $:
$$
\text{discriminant}_d = \text{rand}_d \in \{1, 2, \ldots, k\}
$$

#### c) **Identifying the Direction of Maximum Variance**

This approach selects the dimension along which the variance of the data points is maximized. Mathematically, for each dimension $ i $, the variance $ \sigma_i^2 $ of the data points $ \{ x_1, x_2, \ldots, x_n \} $ is calculated along that dimension:
$$
\sigma_i^2 = \frac{1}{n} \sum_{j=1}^{n} (x_{j,i} - \mu_i)^2
$$
where $ x_{j,i} $ is the $ i $-th coordinate of the $ j $-th point, and $ \mu_i $ is the mean of the coordinates along dimension $ i $:
$$
\mu_i = \frac{1}{n} \sum_{j=1}^{n} x_{j,i}
$$
The dimension with the highest variance $ \sigma_i^2 $ is chosen as the discriminant.

#### d) **The Discriminant is Perpendicular to the Longest Side of the Minimum Bounding Rectangle (Widest Interval)**

Here, the discriminant dimension is chosen such that it is perpendicular to the longest side of the **minimum bounding rectangle** (MBR) that encloses the data. The MBR is defined by the minimum and maximum values along each dimension:
$$
\text{MBR}_i = [\min(x_{1,i}, x_{2,i}, \ldots, x_{n,i}), \max(x_{1,i}, x_{2,i}, \ldots, x_{n,i})]
$$
The dimension $ i $ with the largest difference $ \max(x_{j,i}) - \min(x_{j,i}) $ is selected as the discriminant.

### 3. **Split Position Choice**

Once the discriminant dimension is selected, the **split position** determines where to divide the data in that dimension. The following variants are considered:

#### a) **The Median Value of Our Data Points Across the Chosen Dimension**

The median split is a common approach where the chosen dimension's data points are sorted, and the median value is selected as the split point. Let $ x_1, x_2, \ldots, x_n $ represent the data points along the chosen discriminant dimension. The median $ \text{median}_d $ is defined as:
$$
\text{median}_d = \text{median}(x_1, x_2, \ldots, x_n)
$$
For an odd number of data points, this is the middle value after sorting. For an even number, it is typically the average of the two middle values.

#### b) **The Mean Value of Our Data Points Across the Chosen Dimension**

The mean is calculated as the average of the data points along the chosen dimension. Let $ x_1, x_2, \ldots, x_n $ be the data points in the discriminant dimension. The mean $ \mu_d $ is:
$$
\mu_d = \frac{1}{n} \sum_{i=1}^{n} x_{i,d}
$$
This value is used as the split position.

#### c) **Random Value in the Interval Between the Maximum and Minimum Values of Our Data Points Across the Chosen Dimension (Baseline)**

In this case, a random value $ s_d $ is selected between the minimum and maximum values of the data along the chosen dimension. Specifically, if the minimum value is $ \min(x_1, x_2, \ldots, x_n) $ and the maximum value is $ \max(x_1, x_2, \ldots, x_n) $, the split position is:
$$
s_d = \text{rand} \left( \min(x_1, x_2, \ldots, x_n), \max(x_1, x_2, \ldots, x_n) \right)
$$
where $ \text{rand}(a, b) $ generates a random value between $ a $ and $ b $.

#### d) **Geometric Center: (Maximum Value + Minimum Value) / 2**

The geometric center is a deterministic split where the midpoint between the maximum and minimum values along the discriminant dimension is chosen. Mathematically, if $ \min(x_1, x_2, \ldots, x_n) $ is the minimum value and $ \max(x_1, x_2, \ldots, x_n) $ is the maximum value along the discriminant dimension, the split position is:
$$
\text{split position} = \frac{\min(x_1, x_2, \ldots, x_n) + \max(x_1, x_2, \ldots, x_n)}{2}
$$

### 4. **Summary of Key Formulas**

- **Discriminant Selection**:
  - Alternating: $ \text{discriminant}_d = D[(d-1) \mod k + 1] $
  - Random: $ \text{discriminant}_d = \text{rand}_d \in \{1, 2, \ldots, k\} $
  - Maximum Variance: Select dimension with maximum variance $ \sigma_i^2 $
  - Widest Interval: Select dimension with maximum difference $ \max(x_{j,i}) - \min(x_{j,i}) $

- **Split Position Selection**:
  - Median: $ \text{median}_d = \text{median}(x_1, x_2, \ldots, x_n) $
  - Mean: $ \mu_d = \frac{1}{n} \sum_{i=1}^{n} x_{i,d} $
  - Random: $ s_d = \text{rand}(\min(x_1, x_2, \ldots, x_n), \max(x_1, x_2, \ldots, x_n)) $
  - Geometric Center: $ \text{split position} = \frac{\min(x_1, x_2, \ldots, x_n) + \max(x_1, x_2, \ldots, x_n)}{2} $

### 5. **Computational Complexity Considerations**

The choice of **discriminant** and **split position** directly impacts the time complexity of constructing the KD-Tree. For each node:
- The **median split** and **variance-based discriminant** require sorting, which takes $ O(n \log n) $ time.
- **Random** or **geometric center splits** are computed in $ O(n) $ time, but may not yield as balanced partitions.

In general, the overall complexity of building a KD-Tree is $ O(n \log n) $, assuming balanced splits are achieved. However, if the splits are not balanced (e.g., random splitting), the complexity can degrade to $ O(n^2) $ in the worst case.