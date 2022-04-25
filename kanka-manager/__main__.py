from arguments import get_parser
from kankaclient.client import KankaClient

def get(args, kankaclient):
    print(kankaclient.get(args.entity))

commands = {
    'get': get
}

def main():
    # Parse Args
    args = get_parser()
    # Get config
    # Init client
    client = KankaClient(
        token='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNjUxYzNkNDk1ZjVjZTUzMWQxMjc3MTk5Y2NlMzE1N2U4ZTFkMzZlOWRiYWZiOTY1ZGEyYmI5MTVkZjhkZDFkNTNkZGZlNDhmZTFmZWMzYjMiLCJpYXQiOjE2NDY0NTU3MDguMDA2Mjc4LCJuYmYiOjE2NDY0NTU3MDguMDA2MjgzLCJleHAiOjE2Nzc5OTE3MDcuOTk1NDY5LCJzdWIiOiIzMzM2MiIsInNjb3BlcyI6W119.BsK_qRFoPIlDnNG7DemtD_cVfN98LS-i3f9QUhfm_J7mS7_ltzuJ3typrPL_4lyqbnkrjjx0r5oICRqvgs902AmIDzt-bCGxsyesMWGQcQXFfoahGyJlYfRe4QSNsjlj3cLsM22dn0limMtnKB0I-7XcrbmNU15UJAN0MYJDOZ2pfCmjpn-5GnhgJQNwZrCZc33afUZSVvN_FAYT54GMPExMY0z1J1Zo49uUfs6FQhSG_SNrQ8zbPArCaGgH9hwMIEEhk0dn8-Kv-7SjJu1y4utWs3i9F08-WmIZ9YjDerJsrySc_N6TCgFn2GIeEnb_c-S3RpG4K3PMCTSrOGIKvy_S5zLYZOn6lNXaJ2RTaOhpZvHQHX_OeccoRJ5H9_K5ma1DXBPWaXgujCdaAi5S860ZRqsa8OUSQvHEsq03TNaOKupImBSKLGN6r3Qc57iBTfk6VrOIAO3cFG5Qej7t0gKQdpkDDPAK8dnLvC9QxrfKQCJcfwOrXz7dmUNb-XAKydU2brpqRzJyP3EScShrwPpYgXvE1BJNxtejpPhpE8GCM5TS6-qmHymHILYG0SsoM5HMrA70vFGu3DAJVkRzRavGEBsh_0mFzKR64zNT4hFFEzLyLha5c0FnkgKIFjUfZyrmskRW0t0DifJF5ZGX95PRezeNQHpRZ4yM5G3YseQ',
        campaign='Journey to Morrivir'
    )
    # Execute command
    commands.get(args.command)(args, client)

if __name__ == '__main__':
    main()