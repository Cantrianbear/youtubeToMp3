from contextlib import contextmanager
import io, sys, os
import unittest

from youtubeToMp3.youtube_to_mp3 import Audio

@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class MockMkdir(object):
    def __init__(self):
        self.received_args = None
    def __call__(self, *args):
        self.received_args = args

@contextmanager
def mock_mkdir():
    new_mkdir = MockMkdir
    old_mkdir = os.makedirs
    try:
        os.makedirs = new_mkdir()
        yield os.makedirs
    finally:
        os.makedirs = old_mkdir

class TestYoutubeToMp3(unittest.TestCase):
    
    def assert_usage(self,output):
        self.assertEqual(output, 'youtube_to_mp3.py -l <links separated via comma> [-o <output name>] [-f <folder>]')
        
    def test_no_arguments(self):
        self.assertFalse(Audio('')._Audio__parse_arguments())

    def test_no_arguments_help(self):
        with captured_output() as (out, err):
            Audio([])._Audio__parse_arguments()
        output = out.getvalue().strip()
        self.assert_usage(output)

    def test_usage_help(self):
        with captured_output() as (out, err):
            Audio(['-h'])._Audio__parse_arguments()
        output = out.getvalue().strip()
        self.assert_usage(output)

    def test_only_link_argument(self):
        self.assertTrue(Audio(['-l','http:\\link.com'])._Audio__parse_arguments())

    def test_only_link_argument_name(self):
        audio = Audio(['-l','http:\\link.com'])
        audio._Audio__parse_arguments()
        self.assertEqual(audio.links, ['http:\\link.com'])

    def test_multiple_link_names(self): 
        audio = Audio(['-l','http:\\link.com,http:\\otherlink.com'])
        audio._Audio__parse_arguments()
        self.assertEqual(audio.links, ['http:\\link.com','http:\\otherlink.com'])

    def test_only_output(self):
        self.assertFalse(Audio(['-o','output.kra'])._Audio__parse_arguments())

    def test_output_name(self):
        audio = Audio(['-o','output.wha'])
        audio._Audio__parse_arguments()
        self.assertEqual(audio.output, 'output.wha')

    def test_only_output_help(self):
        with captured_output() as (out, err):
            Audio(['-o', 'output.bla'])._Audio__parse_arguments()
        output = out.getvalue().strip()
        self.assert_usage(output)

    def test_only_folder(self):
        with mock_mkdir():
            self.assertFalse(Audio(['-f','The Cows'])._Audio__parse_arguments())

    def test_folder_name(self):
        with mock_mkdir():
            audio = Audio(['-f','The Cows'])
            audio._Audio__parse_arguments()
        self.assertEqual(audio.folder, os.path.join(os.getcwd(), 'The Cows'))
        
    def test_only_folder_help(self):
        with captured_output() as (out, err):
            with mock_mkdir():
                Audio(['-f', 'The Cows'])._Audio__parse_arguments()
        output = out.getvalue().strip()
        self.assert_usage(output)
        
    def test_default_folder(self):
        audio = Audio(['-l', 'https:\\link.com'])
        audio._Audio__parse_arguments()
        self.assertEqual(audio.folder, os.path.join(os.getcwd(), 'Unknown'))
        
    def test_default_output(self):
        audio = Audio(['-l', 'https:\\link.com'])
        audio._Audio__parse_arguments()
        self.assertEqual(audio.output, os.path.join(
            os.path.join(os.getcwd(), 'Unknown'), "%(title)s.%(ext)s"))
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestYoutubeToMp3)
unittest.TextTestRunner(verbosity=2).run(suite)
