"""
Downsampling algorithms for large datasets.

Provides efficient algorithms to reduce the number of data points
while preserving the visual characteristics of the data.
"""

import numpy as np
from datetime import datetime
from typing import Sequence


def lttb_downsample(
    x: np.ndarray | Sequence,
    y: np.ndarray | Sequence,
    threshold: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Largest Triangle Three Buckets (LTTB) downsampling algorithm.
    
    This algorithm reduces the number of data points while preserving
    the visual shape of the data. It works by dividing data into buckets
    and selecting the point in each bucket that forms the largest triangle
    with the selected points from adjacent buckets.
    
    Args:
        x: X values (can be dates, numbers, or any sequence)
        y: Y values (numeric)
        threshold: Target number of points after downsampling
        
    Returns:
        Tuple of (downsampled_x, downsampled_y) as numpy arrays
        
    Notes:
        - If threshold >= len(data), returns original data unchanged
        - Algorithm preserves first and last points
        - Time complexity: O(n)
        - Particularly effective for time series visualization
        
    Example:
        >>> x = np.arange(100000)
        >>> y = np.sin(x / 1000) + np.random.random(100000) * 0.1
        >>> x_down, y_down = lttb_downsample(x, y, threshold=1000)
        >>> len(x_down)
        1000
    """
    # Convert to numpy arrays if needed
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=np.float64)
    
    n = len(y_arr)
    
    # If threshold is 0 or negative, return original
    if threshold <= 0:
        return x_arr, y_arr
    
    # If data is smaller than threshold, return as-is
    if n <= threshold:
        return x_arr, y_arr
    
    # Threshold must be at least 2 (first and last points)
    if threshold < 2:
        threshold = 2
    
    # Convert x to numeric for calculations (handle datetime)
    if len(x_arr) > 0 and isinstance(x_arr[0], datetime):
        x_numeric = np.array([d.timestamp() for d in x_arr])
    else:
        x_numeric = np.asarray(x_arr, dtype=np.float64)
    
    # Allocate output arrays
    sampled_x = np.empty(threshold, dtype=x_arr.dtype)
    sampled_y = np.empty(threshold, dtype=np.float64)
    
    # Always include first point
    sampled_x[0] = x_arr[0]
    sampled_y[0] = y_arr[0]
    
    # Bucket size (excluding first and last points)
    bucket_size = (n - 2) / (threshold - 2)
    
    # Index for output
    out_idx = 1
    
    # Previous selected point
    prev_x = x_numeric[0]
    prev_y = y_arr[0]
    
    for i in range(threshold - 2):
        # Calculate bucket boundaries
        bucket_start = int((i) * bucket_size) + 1
        bucket_end = int((i + 1) * bucket_size) + 1
        
        # Calculate next bucket's average point (for triangle calculation)
        next_bucket_start = int((i + 1) * bucket_size) + 1
        next_bucket_end = int((i + 2) * bucket_size) + 1
        
        if next_bucket_end > n - 1:
            next_bucket_end = n - 1
            
        # Average of next bucket
        next_avg_x = np.mean(x_numeric[next_bucket_start:next_bucket_end + 1])
        next_avg_y = np.mean(y_arr[next_bucket_start:next_bucket_end + 1])
        
        # Find point in current bucket with largest triangle area
        max_area = -1.0
        max_idx = bucket_start
        
        for j in range(bucket_start, min(bucket_end, n - 1)):
            # Calculate triangle area using cross product
            # Area = 0.5 * |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|
            area = abs(
                (prev_x - next_avg_x) * (y_arr[j] - prev_y) -
                (prev_x - x_numeric[j]) * (next_avg_y - prev_y)
            )
            
            if area > max_area:
                max_area = area
                max_idx = j
        
        # Store selected point
        sampled_x[out_idx] = x_arr[max_idx]
        sampled_y[out_idx] = y_arr[max_idx]
        
        # Update previous point
        prev_x = x_numeric[max_idx]
        prev_y = y_arr[max_idx]
        
        out_idx += 1
    
    # Always include last point
    sampled_x[threshold - 1] = x_arr[n - 1]
    sampled_y[threshold - 1] = y_arr[n - 1]
    
    return sampled_x, sampled_y


def simple_downsample(
    x: np.ndarray | Sequence,
    y: np.ndarray | Sequence,
    threshold: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simple downsampling by taking every nth point.
    
    This is faster than LTTB but may miss important features like peaks.
    
    Args:
        x: X values
        y: Y values
        threshold: Target number of points
        
    Returns:
        Tuple of (downsampled_x, downsampled_y)
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)
    
    n = len(y_arr)
    
    if threshold <= 0 or n <= threshold:
        return x_arr, y_arr
    
    # Calculate step size
    step = max(1, n // threshold)
    
    indices = np.arange(0, n, step)
    
    # Ensure we include the last point
    if indices[-1] != n - 1:
        indices = np.append(indices, n - 1)
    
    return x_arr[indices], y_arr[indices]


def minmax_downsample(
    x: np.ndarray | Sequence,
    y: np.ndarray | Sequence,
    threshold: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Min-max downsampling that preserves peaks and valleys.
    
    For each bucket, includes both the minimum and maximum values,
    ensuring peaks and valleys are preserved.
    
    Args:
        x: X values
        y: Y values  
        threshold: Target number of points (will be approximately 2x buckets)
        
    Returns:
        Tuple of (downsampled_x, downsampled_y)
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y, dtype=np.float64)
    
    n = len(y_arr)
    
    if threshold <= 0 or n <= threshold:
        return x_arr, y_arr
    
    # Number of buckets (each bucket produces 2 points: min and max)
    n_buckets = threshold // 2
    bucket_size = n / n_buckets
    
    result_x = []
    result_y = []
    
    for i in range(n_buckets):
        start = int(i * bucket_size)
        end = int((i + 1) * bucket_size)
        
        if end > n:
            end = n
        if start >= end:
            continue
            
        bucket_y = y_arr[start:end]
        min_idx = start + np.argmin(bucket_y)
        max_idx = start + np.argmax(bucket_y)
        
        # Add in order (min first if it comes first in data)
        if min_idx <= max_idx:
            result_x.extend([x_arr[min_idx], x_arr[max_idx]])
            result_y.extend([y_arr[min_idx], y_arr[max_idx]])
        else:
            result_x.extend([x_arr[max_idx], x_arr[min_idx]])
            result_y.extend([y_arr[max_idx], y_arr[min_idx]])
    
    return np.array(result_x), np.array(result_y)
