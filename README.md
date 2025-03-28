# Bloom-Filters

## Core Tradeoffs

The Bloom filter trades off accuracy (due to false positives) for efficiency in space and time.

## What is Guaranteed

It is guarnteed that there are no false negatives i.e an item said to be a member of a given set
although in fact it is not. This kind of property is necessary for not a few applications.

## Use Cases

The use cases patterns for the bloom filter is when accessing the underlying storage is expensive e.g:

- Membership Testing (Set Membership)
- Database Query Optimization
- Web Caching
- Other

## Things to Explore
1. How does a lightweight Bitcoin client use Bloom filters to check if a transaction with a given TXID likely exists in a block?
2. Any other ways that achieve similar thing functional/non-funcation requirements given different tradeoffs?

## Things to Brush Up On
1. How are derivatives used to calculate minimum and maximum points?
