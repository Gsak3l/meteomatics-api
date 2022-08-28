import server
import collect_api_data

if __name__ == '__main__':
    collect_api_data.run()
    server.run_server()
