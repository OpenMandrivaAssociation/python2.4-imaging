%define py_platsitedir         %(python2.4 -c 'import distutils.sysconfig; print distutils.sysconfig.get_python_lib(plat_specific=1)' 2>/dev/null || echo PYTHON-LIBDIR-NOT-FOUND)
%define name python2.4-imaging
%define version 1.1.6
%define release %mkrel 5

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	Python's own image processing library 
License:	MIT style
Group:		Development/Python
URL:		http://www.pythonware.com/products/pil/

Source0:	http://www.pythonware.com/downloads/Imaging-%{version}.tar.bz2 
Source1:	pil-handbook.pdf.bz2
Source2:	linux-python-paint-icon.gif
Patch0:     %{name}-1.1.6-lib64.patch
Requires:	python2.4
Requires:	tkinter2.4
Requires:	libjpeg >= 6b
Requires:	zlib >= 1.1.2
Requires:	libpng >= 1.0.1
BuildRequires:	python2.4-devel
BuildRequires:	tkinter2.4
BuildRequires:	jpeg-devel >= 6b
BuildRequires:	png-devel >= 1.0.1
BuildRequires:	X11-devel
BuildRequires:	freetype2-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	libsane-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Python Imaging Library version %{version}
   
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%package devel
Summary:	Header files for python-imaging
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
Header files for the Python Imaging Library version %{version}.

%prep
%setup -q -n Imaging-%{version}
bzcat %SOURCE1 > pil-handbook.pdf
%patch0 -p 1 -b .lib64

%build
python2.4 setup.py build_ext -i
cd Sane
python2.4 setup.py build_ext -i

%install
rm -fr %{buildroot}
find . -type f | xargs perl -pi -e 's@/usr/local/bin/python@/usr/bin/python@'

python2.4 setup.py install --root=%{buildroot}
pushd libImaging
mkdir -p  %{buildroot}%{_includedir}/python2.4
install -m 644 ImPlatform.h Imaging.h %{buildroot}%{_includedir}/python2.4
popd

cd Sane
python2.4 setup.py install --root=%{buildroot}
cd ..

# prevent conflict with normal python-imaging package
for bin in %{buildroot}%{_bindir}/*; do
    mv $bin %{buildroot}%{_bindir}/`basename $bin .py`2.4.py
done

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc pil-handbook.pdf Scripts Images CHANGES* README
%{_bindir}/pil*.py
%py_platsitedir/PIL.pth
%dir %py_platsitedir/PIL
%py_platsitedir/PIL/*.py*
%py_platsitedir/PIL/_imaging.so
%py_platsitedir/PIL/_imagingft.so
%py_platsitedir/PIL/_imagingmath.so
%py_platsitedir/PIL/_imagingtk.so
%py_platsitedir/_sane.so
%py_platsitedir/sane.py
%py_platsitedir/sane.pyc

%files devel
%defattr (-,root,root)
%{_includedir}/python2.4/Imaging.h
%{_includedir}/python2.4/ImPlatform.h
