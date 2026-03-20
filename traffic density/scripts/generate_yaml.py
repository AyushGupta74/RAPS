def generate_yaml():
    import yaml,os
    from utils.class_map import CLASS_MAP

    data_yaml_content = {
        'path': '../traffic_density_project/data/processed',  
        'train': 'images/train',  
        'val': 'images/val',
        'nc': len(set(CLASS_MAP.values()))  
    }

    seen = set()
    ordered_class_names = []
    for k, v in sorted(CLASS_MAP.items(), key=lambda item: item[1]):
        if v not in seen:
            ordered_class_names.append(k)
            seen.add(v)

    # Convert the ordered_class_names list to a dictionary with integer keys
    names_dict = {i: name for i, name in enumerate(ordered_class_names)}
    data_yaml_content['names'] = names_dict

    yaml_output_dir = 'configs'
    os.makedirs(yaml_output_dir, exist_ok=True)
    yaml_file_path = os.path.join(yaml_output_dir, 'traffic.yaml')

    # Write the dictionary to a YAML file
    with open(yaml_file_path, 'w') as f:
        yaml.dump(data_yaml_content, f, default_flow_style=False)

    print(f"YOLO data.yaml created at: {yaml_file_path}")
    print("Content of data.yaml:")
    with open(yaml_file_path, 'r') as f:
        print(f.read())
