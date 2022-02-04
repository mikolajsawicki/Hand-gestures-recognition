from distutils.core import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Hand-gestures-recognition',
    packages=['hand_gestures_recognition', 'hand_gestures_recognition_qt'],
    version='0.1.1',
    description='An app for hand gesture recognition.',
    author='Mikolaj Sawicki',
    author_email='msawicki9999@gmail.com',
    license='GNU General Public License v3.0',
    # scripts=['bin/'],
    url='https://github.com/mikolajsawicki/Hand-gestures-recognition',
    long_description=long_description,
    install_requires=['numpy', 'opencv-python', 'tensorflow', 'PyQt5', 'mediapipe', 'scikit-learn'],
    download_url='https://github.com/mikolajsawicki/Hand-gestures-recognition',
    keywords=['hand', 'gesture', 'recognition', 'cnn', 'mediapipe', 'random forest', 'machine learning'],
    python_requires='>=3',
    setup_requires=['wheel'],
    long_description_content_type="text/markdown",
    include_package_data=True,
)