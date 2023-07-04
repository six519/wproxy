import argparse

from . import WProxy


def run():
    parser = argparse.ArgumentParser(description='Websocket proxy')
    parser.add_argument('--host', help='Proxy host', default="0.0.0.0")
    parser.add_argument('--port', help='Proxy port', default=8765)
    parser.add_argument('--url', help='Websocket URL to proxy')
    parser.add_argument('--ssl_cert', help='SSL Certificate')
    parser.add_argument('--ssl_key', help='SSL Key')
    parser.add_argument('--headers', help='Extra HTTP headers', nargs='*')

    args = parser.parse_args()

    this_proxy = WProxy(
        host=args.host,
        port=args.port,
        url=args.url,
        ssl_cert=args.ssl_cert,
        ssl_key=args.ssl_key,
    )

    this_proxy.load_headers_from_args(args.headers)
    this_proxy.run()