import json

with open(r'\\192.168.29.60\workflows\Images_workflow.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find nodes with widgets
for node in data['nodes']:
    if node.get('widgets_values'):
        node_id = node.get('id')
        node_type = node.get('type')
        inputs = node.get('inputs', [])
        widgets = node.get('widgets_values', [])
        
        print(f'\nNode {node_id} ({node_type}):')
        print(f'  Total inputs: {len(inputs)}')
        print(f'  Total widgets: {len(widgets)}')
        
        # Show inputs with widget flag
        widget_count = 0
        for i, inp in enumerate(inputs):
            if isinstance(inp, dict):
                has_widget = 'widget' in inp
                has_link = 'link' in inp
                inp_name = inp.get('name', 'unknown')
                print(f'    Input {i}: {inp_name} (widget={has_widget}, link={has_link})')
                
                if has_widget and not has_link and widget_count < len(widgets):
                    print(f'      -> Widget value: {widgets[widget_count]}')
                    widget_count += 1
        
        if node_id > 450:  # Stop after a few samples
            break
