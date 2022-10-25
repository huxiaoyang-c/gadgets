import re
import requests

from bs4 import BeautifulSoup
from tabulate import tabulate


def get_html_node(url, tag, attrs=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features='lxml')
    node = soup.findAll(tag, attrs=attrs)
    return node


def re_find(p, s):
    find = re.findall(p, s)
    assert len(find) == 1
    return find[0]


def get_mmdet_ver_2_mmcv_min_ver():
    mmdet_ver_2_mmcv_min_ver = {}
    node = get_html_node('https://gitee.com/open-mmlab/mmdetection/blob/master/docs/zh_cn/get_started.md',
                         'table')[0]
    for tr in node.findAll('tr')[1:]:
        tds = tr.findAll('td')
        mmdet_ver = tds[0].text
        mmcv_ver = tds[1].text
        mmcv_ver = re.findall('(\d+.\d+.\d+)', mmcv_ver)[0]
        mmdet_ver_2_mmcv_min_ver[mmdet_ver] = mmcv_ver
    return mmdet_ver_2_mmcv_min_ver


def get_torch_ver_2_cuda_ver_2_install_mmcv():
    torch_ver_2_cuda_ver_2_install_mmcv = {}
    node = get_html_node('https://gitee.com/open-mmlab/mmcv', 'table')[0]

    for span in node.findAll('span', attrs={'id': 'LC1', 'class': 'line'}):
        span = span.text.strip()
        if 'cpu' in span:
            continue
        torch_ver = re_find('torch(\d\.\d+\.\d)', span)
        cuda_ver = re_find('cu(\d+)', span)
        cuda_ver_str = str(cuda_ver)
        cuda_ver = cuda_ver_str[:-1] + '.' + cuda_ver_str[-1]
        torch_ver_2_cuda_ver_2_install_mmcv.setdefault(torch_ver, {})
        torch_ver_2_cuda_ver_2_install_mmcv[torch_ver][cuda_ver] = span

    return torch_ver_2_cuda_ver_2_install_mmcv


def get_torch_ver_2_cuda_ver_2_install_torch():
    torch_ver_2_cuda_ver_2_install_torch = {}
    node = get_html_node('https://pytorch.org/get-started/previous-versions/',
                         'div', {'class': 'language-plaintext highlighter-rouge'})

    for lines in node:
        lines = lines.text

        # 过滤 conda 安装
        if 'conda' in lines:
            continue
        # 过滤 OSX
        if lines.startswith('pip'):
            continue

        lines = lines.split('\n')
        lines = [line for line in lines if line]  # 过滤空字符串

        # 按 CPU、CUDA 、ROCM 归类安装命令
        commands_dict = {}
        key = ''
        ignore = False
        for line in lines:
            if line.startswith('#'):
                if 'CUDA' in line:
                    key = line
                    commands_dict.setdefault(line, [])
                    ignore = False
                else:
                    ignore = True
            else:
                if ignore:
                    continue
                else:
                    commands_dict[key].append(line)

        # 提取 PyTorch 版本
        torch_versions = []
        cuda_ver_2_install_command = {}
        for k, v in commands_dict.items():
            assert len(v) == 1
            cuda_ver = re_find('CUDA (\d+\.\d)', k)
            cuda_ver_2_install_command[cuda_ver] = v[0]
            torch_ver = re_find('torch==(\d\.\d+\.\d)', v[0])
            torch_versions.append(torch_ver)
        assert len(set(torch_versions)) == 1
        torch_ver = torch_versions[0]
        torch_ver_2_cuda_ver_2_install_torch[torch_ver] = cuda_ver_2_install_command
        if torch_ver == '1.5.0':
            break
    return torch_ver_2_cuda_ver_2_install_torch


def main():
    torch_ver_2_cuda_ver_2_install_torch_dict = get_torch_ver_2_cuda_ver_2_install_torch()

    torch_ver_2_cuda_ver_2_install_mmcv_dict = get_torch_ver_2_cuda_ver_2_install_mmcv()

    mmdet_ver_2_mmcv_min_ver_dict = get_mmdet_ver_2_mmcv_min_ver()
    del mmdet_ver_2_mmcv_min_ver_dict['2.3.0rc0']
    del mmdet_ver_2_mmcv_min_ver_dict['master']

    optional_torch_versions = sorted(list(torch_ver_2_cuda_ver_2_install_torch_dict.keys()),
                                     key=lambda v: float('.'.join(v.split('.')[1:])))
    print(f'PyTorch: {" | ".join(optional_torch_versions)}')
    torch_version = input(f'>>> ')

    cuda_ver_2_install_torch_dict = torch_ver_2_cuda_ver_2_install_torch_dict[torch_version]
    optional_cuda_versions = sorted(list(cuda_ver_2_install_torch_dict.keys()),
                                    key=lambda v: float(v))
    print(f'CUDA: {" | ".join(optional_cuda_versions)}')
    cuda_version = input(f'>>> ')

    optional_mmdet_versions = sorted(list(mmdet_ver_2_mmcv_min_ver_dict.keys()),
                                     key=lambda v: float('.'.join(v.split('.')[1:])))
    print(f'MMDetection: {" | ".join(optional_mmdet_versions)}')
    mmdet_version = input('>>> ')
    mmcv_version = mmdet_ver_2_mmcv_min_ver_dict[mmdet_version]
    torch_version_for_mmcv = '.'.join(torch_version.split('.')[:2]) + '.0'

    install_torch = torch_ver_2_cuda_ver_2_install_torch_dict[torch_version][cuda_version]
    install_mmcv = torch_ver_2_cuda_ver_2_install_mmcv_dict[torch_version_for_mmcv][cuda_version]

    table_header = ['Package', 'Install Command']
    table_data = [
        ['PyTorch', install_torch],
        ['MMCV', install_mmcv.replace('{mmcv_version}', mmcv_version)]
    ]
    print(tabulate(table_data, headers=table_header, tablefmt='fancy_grid'))
