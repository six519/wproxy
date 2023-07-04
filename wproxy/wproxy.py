import ssl
import asyncio

import websockets


class WProxy(object):
    
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host', '0.0.0.0')
        self.port = kwargs.get('port', 8765)
        self.url = kwargs.get('url', '')
        self.ssl_cert = kwargs.get('ssl_cert', '')
        self.ssl_key = kwargs.get('ssl_key', '')
        self.extra_headers = kwargs.get('extra_headers', {})
        self.ssl_context = None

        if not self.url:
            raise Exception("Please specify url")
        
        if self.ssl_cert and self.ssl_key:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(self.ssl_cert, keyfile=self.ssl_key)

    def load_headers_from_args(self, headers):
        if headers is not None:
            for header in headers:
                split_str = header.split(":")
                self.extra_headers[split_str[0].strip()] = split_str[1].strip()
        
    async def __send_message(self, from_server, to_server):
        async for message in from_server:
            await to_server.send(message)

    async def __on_connection(self, websocket, path):
        loop = asyncio.get_event_loop()
        this_url = self.url + path
        async with websockets.connect(this_url) as ws:
            client_to_server = loop.create_task(self.__send_message(ws, websocket))
            server_to_client = loop.create_task(self.__send_message(websocket, ws))
            await client_to_server
            await server_to_client

    def run(self):
        server = websockets.serve(self.__on_connection, self.host, self.port, ssl=self.ssl_context, extra_headers=self.extra_headers)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()