from project.modules.input_drone_data.drone_data_receiver_module import DroneDataReceiverModule


if __name__ == '__main__':
    """
    The main function testing for the module.
    """
    drone_data_receiver_module = DroneDataReceiverModule(
        drone_video_file_path='pendiente...',
        drone_data_db_file_path='/home/charly/Documentos/universidad/Modular/proyecto-modular/project/comms/flights/2021-11-03-17_50_42.db',
        drone_data_json_file_path='/home/charly/Documentos/universidad/Modular/proyecto-modular/project/comms/flights/2021-11-03-17_50_42.json')
    drone_data_receiver_module.load_module()
