######### Custom Defined Macros ##########
# pkg_name - The name of the source Python package. (%{pkg_name})
# pkg_version - The version number to assign the RPM. (%{pkg_version})
# pkg_release - The release number to assign the RPM. (%{pkg_release})
# pkg_summary - The short summary of the package. (%{pkg_summary})
# pkg_group - The RPM group in which the package belongs. (%{pkg_version})
# pkg_license - The distribution license for the package. (%{pkg_license})
# pkg_url - The URL to the package source. (%{pkg_url})
# pkg_source - The name of the artifact in SOURCES to use. (%{pkg_source})
# pkg_install_dir - The absolute path where the package will be installed. (%{pkg_install_dir})
# pkg_user - The user who will own the installed files. (%{pkg_user})
# pkg_user_group - The grou which will own the installed files. (%{pkg_user_group})
###########################################

%define final_installation_dir %{pkg_install_dir}/%{name}
%define venv_dir %{buildroot}/%{final_installation_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip {% for option in pip_options %}{{ option }} {% endfor %}

# Disable automatic bytecode compiling to save space and time.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Disable automatic requires and provides gathering.
# These don't work well with a venv.
AutoReq: No
AutoProv: No

Name: %{pkg_name}
Version: %{pkg_version}
Release:    %{pkg_release}
Summary: %{pkg_summary}

Group: %{pkg_group}
License: %{pkg_license}
URL: %{pkg_url}
Source0: %{pkg_source}
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
{{ description }}

%prep
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{pkg_install_dir}


%build
%install
# Create a virtualenv to contain to the package code.
virtualenv %{venv_dir} {% for option in venv_options %}{{ option }} {% endfor %}

# Ensure pip and setuptools are at the latest versions.
%{venv_pip} install -U pip setuptools

# Install any Python dependencies.
{% for requirement in requirements %}
%{venv_pip} install -r %{SOURCE0}/{{ requirement }}
{% endfor %}

# Install the source package.
pushd %{SOURCE0}
%{venv_python} setup.py install
popd

# RECORD files are used by wheels for checksum. They contain path names which
# match the buildroot and must be removed or the package will fail to build.
find %{buildroot} -name "RECORD" -exec rm -rf {} \;

# Change the virtualenv path to the target installation direcotry.
venvctrl-relocate --source=%{buildroot}/%{final_installation_dir} --destination=/%{final_installation_dir}

# Copy over any custom files.
{% for source, destination in extra_files %}
mkdir -p "%{buildroot}/%(dirname {{ destination }})"
cp -R %{SOURCE0}/{{ source }} %{buildroot}/{{ destination }}
{% endfor %}

%clean
rm -rf %{buildroot}


%files
%defattr(-,%{pkg_user},%{pkg_user_group},-)
/%{final_installation_dir}
{% for source, destination in extra_files %}
/{{ destination }}
{% endfor %}


%changelog

%post
id -u %{pkg_user} &>/dev/null || useradd %{pkg_user}
id -g %{pkg_user_group} &>/dev/null || groupadd %{pkg_user_group}
chown -R %{pkg_user}:%{pkg_user_group} /%{final_installation_dir}
{% for source, destination in extra_files %}
chown -R %{pkg_user}:%{pkg_user_group} /{{ destination }}
{% endfor %}
{% for post in posts %}
{{ post }}
{% endfor %}

%postun
if [[ "$1" == "0" ]]; then
    rm -rf /%{final_installation_dir}
fi
{% for postun in postuns %}
{{ postun }}
{% endfor %}
