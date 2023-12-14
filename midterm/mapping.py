def linear_mapping(blocks, processors):
    mapping = []
    for i, block in enumerate(blocks):
        processor = i % processors
        mapping.append((block, processor))
    return mapping




# Example usage
blocks = ['Block1', 'Block2', 'Block3', 'Block4', 'Block5', 'Block6', 'Block7', 'Block8', 'Block9' ]
processors = 3

mapping = linear_mapping(blocks, processors)
for block, processor in mapping:
    print(f"{block} is mapped to Processor {processor}")