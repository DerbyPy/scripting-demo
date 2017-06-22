import mock
from sh import uname, dpkg


def filter_packages(dpkg_output, kernel_version):
    packages_list = dpkg_output.strip().splitlines()

    installed_lines = filter(lambda line: line.startswith('ii'), packages_list)
    package_names = [line.split()[1] for line in installed_lines]

    return filter(lambda package: kernel_version not in package, package_names)


def main():
    dpkg_output = dpkg('-l', 'linux-image-[0-9]*', 'linux-headers-[0-9]*', _env={'COLUMNS': '200'})

    uname_output = uname('-r').strip()  # like 4.4.0-79-generic
    kernel_version = uname_output.rsplit('-', 1)[0]
    print('kernel version:', kernel_version)

    removed_packages = filter_packages(dpkg_output, kernel_version)
    print('\n'.join(removed_packages))


if __name__ == '__main__':
    main()


class TestFilterPackages:

    def test_installed_filter(self):
        dpkg_output = 'rc  linux-image-1.1.1-11-generic aaa 111\n' \
            'ii  linux-image-1.1.1-12-generic aaa 111\n'

        packages = filter_packages(dpkg_output, 'abc')

        assert list(packages) == ['linux-image-1.1.1-12-generic']

    def test_kernel_version_filter(self):
        dpkg_output = 'ii  linux-image-1.1.1-11-generic aaa 111\n' \
            'ii  linux-image-1.1.1-12-generic aaa 111\n'

        packages = filter_packages(dpkg_output, '1.1.1-11')

        assert list(packages) == ['linux-image-1.1.1-12-generic']


class TestMain:

    @mock.patch('kernel-list-11.print')
    @mock.patch('kernel-list-11.uname')
    @mock.patch('kernel-list-11.dpkg')
    def test_ok(self, m_dpkg, m_uname, m_print):
        dpkg_output = 'ii  linux-image-1.1.1-11-generic aaa 111\n' \
            'ii  linux-image-1.1.1-12-generic aaa 111\n'

        m_dpkg.return_value = dpkg_output
        m_uname.return_value = '1.1.1-11-generic\n'

        main()

        assert m_print.mock_calls == [
            mock.call('kernel version:', '1.1.1-11'),
            mock.call('linux-image-1.1.1-12-generic'),
        ]
