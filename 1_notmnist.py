{

"nbformat": 4,

"nbformat_minor": 0,

"metadata": {

"colab": {

"version": "0.3.2",

"views": {},

"default_view": {},

"name": "1_notmnist.ipynb",

"provenance": []

}

},

"cells": [

{

"cell_type": "markdown",

"metadata": {

"id": "5hIbr52I7Z7U",

"colab_type": "text"

},

"source": [

"Deep Learning\n",

"=============\n",

"\n",

"Assignment 1\n",

"------------\n",

"\n",

"The objective of this assignment is to learn about simple data curation practices, and familiarize you with some of the data we'll be reusing later.\n",

"\n",

"This notebook uses the [notMNIST](http://yaroslavvb.blogspot.com/2011/09/notmnist-dataset.html) dataset to be used with python experiments. This dataset is designed to look like the classic [MNIST](http://yann.lecun.com/exdb/mnist/) dataset, while looking a little more like real data: it's a harder task, and the data is a lot less 'clean' than MNIST."

]

},

{

"cell_type": "code",

"metadata": {

"id": "apJbCsBHl-2A",

"colab_type": "code",

"colab": {

"autoexec": {

"startup": false,

"wait_interval": 0

}

},

"cellView": "both"

},

"source": [

"# These are all the modules we'll be using later. Make sure you can import them\n",

"# before proceeding further.\n",

"from __future__ import print_function\n",

"import imageio\n",

"import matplotlib.pyplot as plt\n",

"import numpy as np\n",

"import os\n",

"import sys\n",

"import tarfile\n",

"from IPython.display import display, Image\n",

"from sklearn.linear_model import LogisticRegression\n",

"from six.moves.urllib.request import urlretrieve\n",

"from six.moves import cPickle as pickle\n",

"\n",

"# Config the matplotlib backend as plotting inline in IPython\n",

"%matplotlib inline"

],

"outputs": [],

"execution_count": 0

},

{

"cell_type": "markdown",

"metadata": {

"id": "jNWGtZaXn-5j",

"colab_type": "text"

},

"source": [

"First, we'll download the dataset to our local machine. The data consists of characters rendered in a variety of fonts on a 28x28 image. The labels are limited to 'A' through 'J' (10 classes). The training set has about 500k and the testset 19000 labeled examples. Given these sizes, it should be possible to train models quickly on any machine."

]

},

{

"cell_type": "code",

"metadata": {

"id": "EYRJ4ICW6-da",

"colab_type": "code",

"colab": {

"autoexec": {

"startup": false,

"wait_interval": 0

},

"output_extras": [

{

"item_id": 1

}

]

},

"cellView": "both",

"executionInfo": {

"elapsed": 186058,

"status": "ok",

"timestamp": 1444485672507,

"user": {

"color": "#1FA15D",

"displayName": "Vincent Vanhoucke",

"isAnonymous": false,

"isMe": true,

"permissionId": "05076109866853157986",

"photoUrl": "//lh6.googleusercontent.com/-cCJa7dTDcgQ/AAAAAAAAAAI/AAAAAAAACgw/r2EZ_8oYer4/s50-c-k-no/photo.jpg",

"sessionId": "2a0a5e044bb03b66",

"userId": "102167687554210253930"

},

"user_tz": 420

},

"outputId": "0d0f85df-155f-4a89-8e7e-ee32df36ec8d"

},

"source": [

"url = 'https://commondatastorage.googleapis.com/books1000/'\n",

"last_percent_reported = None\n",

"data_root = '.' # Change me to store data elsewhere\n",

"\n",

"def download_progress_hook(count, blockSize, totalSize):\n",

" \"\"\"A hook to report the progress of a download. This is mostly intended for users with\n",

" slow internet connections. Reports every 5% change in download progress.\n",

" \"\"\"\n",

" global last_percent_reported\n",

" percent = int(count * blockSize * 100 / totalSize)\n",

"\n",

" if last_percent_reported != percent:\n",

" if percent % 5 == 0:\n",

" sys.stdout.write(\"%s%%\" % percent)\n",

        " sys.stdout.flush()\n",

        " else:\n",

        " sys.stdout.write(\".\")\n",

        " sys.stdout.flush()\n",

        " \n",

        " last_percent_reported = percent\n",

        " \n",

        "def maybe_download(filename, expected_bytes, force=False):\n",

        " \"\"\"Download a file if not present, and make sure it's the right size.\"\"\"\n",

        " dest_filename = os.path.join(data_root, filename)\n",

        " if force or not os.path.exists(dest_filename):\n",

        " print('Attempting to download:', filename) \n",

        " filename, _ = urlretrieve(url + filename, dest_filename, reporthook=download_progress_hook)\n",

        " print('\\nDownload Complete!')\n",

        " statinfo = os.stat(dest_filename)\n",

        " if statinfo.st_size == expected_bytes:\n",

        " print('Found and verified', dest_filename)\n",

        " else:\n",

        " raise Exception(\n",

        " 'Failed to verify ' + dest_filename + '. Can you get to it with a browser?')\n",

        " return dest_filename\n",

        "\n",

        "train_filename = maybe_download('notMNIST_large.tar.gz', 247336696)\n",

        "test_filename = maybe_download('notMNIST_small.tar.gz', 8458043)"

      ],

      "outputs": [

        {

          "output_type": "stream",

          "text": [

            "Found and verified notMNIST_large.tar.gz\n",

            "Found and verified notMNIST_small.tar.gz\n"

          ],

          "name": "stdout"

        }

      ],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "cC3p0oEyF8QT",

        "colab_type": "text"

      },

      "source": [

        "Extract the dataset from the compressed .tar.gz file.\n",

        "This should give you a set of directories, labeled A through J."

      ]

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "H8CBE-WZ8nmj",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          },

          "output_extras": [

            {

              "item_id": 1

            }

          ]

        },

        "cellView": "both",

        "executionInfo": {

          "elapsed": 186055,

          "status": "ok",

          "timestamp": 1444485672525,

          "user": {

            "color": "#1FA15D",

            "displayName": "Vincent Vanhoucke",

            "isAnonymous": false,

            "isMe": true,

            "permissionId": "05076109866853157986",

            "photoUrl": "//lh6.googleusercontent.com/-cCJa7dTDcgQ/AAAAAAAAAAI/AAAAAAAACgw/r2EZ_8oYer4/s50-c-k-no/photo.jpg",

            "sessionId": "2a0a5e044bb03b66",

            "userId": "102167687554210253930"

          },

          "user_tz": 420

        },

        "outputId": "ef6c790c-2513-4b09-962e-27c79390c762"

      },

      "source": [

        "num_classes = 10\n",

        "np.random.seed(133)\n",

        "\n",

        "def maybe_extract(filename, force=False):\n",

        " root = os.path.splitext(os.path.splitext(filename)[0])[0] # remove .tar.gz\n",

        " if os.path.isdir(root) and not force:\n",

        " # You may override by setting force=True.\n",

        " print('%s already present - Skipping extraction of %s.' % (root, filename))\n",

        " else:\n",

        " print('Extracting data for %s. This may take a while. Please wait.' % root)\n",

        " tar = tarfile.open(filename)\n",

        " sys.stdout.flush()\n",

        " tar.extractall(data_root)\n",

        " tar.close()\n",

        " data_folders = [\n",

        " os.path.join(root, d) for d in sorted(os.listdir(root))\n",

        " if os.path.isdir(os.path.join(root, d))]\n",

        " if len(data_folders) != num_classes:\n",

        " raise Exception(\n",

        " 'Expected %d folders, one per class. Found %d instead.' % (\n",

        " num_classes, len(data_folders)))\n",

        " print(data_folders)\n",

        " return data_folders\n",

        " \n",

        "train_folders = maybe_extract(train_filename)\n",

        "test_folders = maybe_extract(test_filename)"

      ],

      "outputs": [

        {

          "output_type": "stream",

          "text": [

            "['notMNIST_large/A', 'notMNIST_large/B', 'notMNIST_large/C', 'notMNIST_large/D', 'notMNIST_large/E', 'notMNIST_large/F', 'notMNIST_large/G', 'notMNIST_large/H', 'notMNIST_large/I', 'notMNIST_large/J']\n",

            "['notMNIST_small/A', 'notMNIST_small/B', 'notMNIST_small/C', 'notMNIST_small/D', 'notMNIST_small/E', 'notMNIST_small/F', 'notMNIST_small/G', 'notMNIST_small/H', 'notMNIST_small/I', 'notMNIST_small/J']\n"

          ],

          "name": "stdout"

        }

      ],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "4riXK3IoHgx6",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 1\n",

        "---------\n",

        "\n",

        "Let's take a peek at some of the data to make sure it looks sensible. Each exemplar should be an image of a character A through J rendered in a different font. Display a sample of the images that we just downloaded. Hint: you can use the package IPython.display.\n",

        "\n",

        "---"

      ]

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "PBdkjESPK8tw",

        "colab_type": "text"

      },

      "source": [

        "Now let's load the data in a more manageable format. Since, depending on your computer setup you might not be able to fit it all in memory, we'll load each class into a separate dataset, store them on disk and curate them independently. Later we'll merge them into a single dataset of manageable size.\n",

        "\n",

        "We'll convert the entire dataset into a 3D array (image index, x, y) of floating point values, normalized to have approximately zero mean and standard deviation ~0.5 to make training easier down the road. \n",

        "\n",

        "A few images might not be readable, we'll just skip them."

      ]

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "h7q0XhG3MJdf",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          },

          "output_extras": [

            {

              "item_id": 30

            }

          ]

        },

        "cellView": "both",

        "executionInfo": {

          "elapsed": 399874,

          "status": "ok",

          "timestamp": 1444485886378,

          "user": {

            "color": "#1FA15D",

            "displayName": "Vincent Vanhoucke",

            "isAnonymous": false,

            "isMe": true,

            "permissionId": "05076109866853157986",

            "photoUrl": "//lh6.googleusercontent.com/-cCJa7dTDcgQ/AAAAAAAAAAI/AAAAAAAACgw/r2EZ_8oYer4/s50-c-k-no/photo.jpg",

            "sessionId": "2a0a5e044bb03b66",

            "userId": "102167687554210253930"

          },

          "user_tz": 420

        },

        "outputId": "92c391bb-86ff-431d-9ada-315568a19e59"

      },

      "source": [

        "image_size = 28 # Pixel width and height.\n",

        "pixel_depth = 255.0 # Number of levels per pixel.\n",

        "\n",

        "def load_letter(folder, min_num_images):\n",

        " \"\"\"Load the data for a single letter label.\"\"\"\n",

        " image_files = os.listdir(folder)\n",

        " dataset = np.ndarray(shape=(len(image_files), image_size, image_size),\n",

        " dataset = np.ndarray(shape=(len(image_files), image_size, image_size),\n",

        " dtype=np.float32)\n",

        " print(folder)\n",

        " num_images = 0\n",

        " for image in image_files:\n",

        " image_file = os.path.join(folder, image)\n",

        " try:\n",

        " image_data = (imageio.imread(image_file).astype(float) - \n",

        " pixel_depth / 2) / pixel_depth\n",

        " if image_data.shape != (image_size, image_size):\n",

        " raise Exception('Unexpected image shape: %s' % str(image_data.shape))\n",

        " dataset[num_images, :, :] = image_data\n",

        " num_images = num_images + 1\n",

        " except (IOError, ValueError) as e:\n",

        " print('Could not read:', image_file, ':', e, '- it\\'s ok, skipping.')\n",

        " \n",

        " dataset = dataset[0:num_images, :, :]\n",

        " if num_images < min_num_images:\n",

        " raise Exception('Many fewer images than expected: %d < %d' %\n",

        " (num_images, min_num_images))\n",

        " \n",

        " print('Full dataset tensor:', dataset.shape)\n",

        " print('Mean:', np.mean(dataset))\n",

        " print('Standard deviation:', np.std(dataset))\n",

        " return dataset\n",

        " \n",

        "def maybe_pickle(data_folders, min_num_images_per_class, force=False):\n",

        " dataset_names = []\n",

        " for folder in data_folders:\n",

        " set_filename = folder + '.pickle'\n",

        " dataset_names.append(set_filename)\n",

        " if os.path.exists(set_filename) and not force:\n",

        " # You may override by setting force=True.\n",

        " print('%s already present - Skipping pickling.' % set_filename)\n",

        " else:\n",

        " print('Pickling %s.' % set_filename)\n",

        " dataset = load_letter(folder, min_num_images_per_class)\n",

        " try:\n",

        " with open(set_filename, 'wb') as f:\n",

        " pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)\n",

        " except Exception as e:\n",

        " print('Unable to save data to', set_filename, ':', e)\n",

        " \n",

        " return dataset_names\n",

        "\n",

        "train_datasets = maybe_pickle(train_folders, 45000)\n",

        "test_datasets = maybe_pickle(test_folders, 1800)"

      ],

      "outputs": [

        {

          "output_type": "stream",

          "text": [

            "notMNIST_large/A\n",

            "Could not read: notMNIST_large/A/Um9tYW5hIEJvbGQucGZi.png : cannot identify image file - it's ok, skipping.\n",

            "Could not read: notMNIST_large/A/RnJlaWdodERpc3BCb29rSXRhbGljLnR0Zg==.png : cannot identify image file - it's ok, skipping.\n",

            "Could not read: notMNIST_large/A/SG90IE11c3RhcmQgQlROIFBvc3Rlci50dGY=.png : cannot identify image file - it's ok, skipping.\n",

            "Full dataset tensor: (52909, 28, 28)\n",

            "Mean: -0.12848\n",

            "Standard deviation: 0.425576\n",

            "notMNIST_large/B\n",

            "Could not read: notMNIST_large/B/TmlraXNFRi1TZW1pQm9sZEl0YWxpYy5vdGY=.png : cannot identify image file - it's ok, skipping.\n",

            "Full dataset tensor: (52911, 28, 28)\n",

            "Mean: -0.00755947\n",

            "Standard deviation: 0.417272\n",

            "notMNIST_large/C\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: -0.142321\n",

            "Standard deviation: 0.421305\n",

            "notMNIST_large/D\n",

            "Could not read: notMNIST_large/D/VHJhbnNpdCBCb2xkLnR0Zg==.png : cannot identify image file - it's ok, skipping.\n",

            "Full dataset tensor: (52911, 28, 28)\n",

            "Mean: -0.0574553\n",

            "Standard deviation: 0.434072\n",

            "notMNIST_large/E\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: -0.0701406\n",

            "Standard deviation: 0.42882\n",

            "notMNIST_large/F\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: -0.125914\n",

            "Standard deviation: 0.429645\n",

            "notMNIST_large/G\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: -0.0947771\n",

            "Standard deviation: 0.421674\n",

            "notMNIST_large/H\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: -0.0687667\n",

            "Standard deviation: 0.430344\n",

            "notMNIST_large/I\n",

            "Full dataset tensor: (52912, 28, 28)\n",

            "Mean: 0.0307405\n",

            "Standard deviation: 0.449686\n",

            "notMNIST_large/J\n",

            "Full dataset tensor: (52911, 28, 28)\n",

            "Mean: -0.153479\n",

            "Standard deviation: 0.397169\n",

            "notMNIST_small/A\n",

            "Could not read: notMNIST_small/A/RGVtb2NyYXRpY2FCb2xkT2xkc3R5bGUgQm9sZC50dGY=.png : cannot identify image file - it's ok, skipping.\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: -0.132588\n",

            "Standard deviation: 0.445923\n",

            "notMNIST_small/B\n",

            "Full dataset tensor: (1873, 28, 28)\n",

            "Mean: 0.00535619\n",

            "Standard deviation: 0.457054\n",

            "notMNIST_small/C\n",

            "Full dataset tensor: (1873, 28, 28)\n",

            "Mean: -0.141489\n",

            "Standard deviation: 0.441056\n",

            "notMNIST_small/D\n",

            "Full dataset tensor: (1873, 28, 28)\n",

            "Mean: -0.0492094\n",

            "Standard deviation: 0.460477\n",

            "notMNIST_small/E\n",

            "Full dataset tensor: (1873, 28, 28)\n",

            "Mean: -0.0598952\n",

            "Standard deviation: 0.456146\n",

            "notMNIST_small/F\n",

            "Could not read: notMNIST_small/F/Q3Jvc3NvdmVyIEJvbGRPYmxpcXVlLnR0Zg==.png : cannot identify image file - it's ok, skipping.\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: -0.118148\n",

            "Standard deviation: 0.451134\n",

            "notMNIST_small/G\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: -0.092519\n",

            "Standard deviation: 0.448468\n",

            "notMNIST_small/H\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: -0.0586729\n",

            "Standard deviation: 0.457387\n",

            "notMNIST_small/I\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: 0.0526481\n",

            "Standard deviation: 0.472657\n",

            "notMNIST_small/J\n",

            "Full dataset tensor: (1872, 28, 28)\n",

            "Mean: -0.15167\n",

            "Standard deviation: 0.449521\n"

          ],

          "name": "stdout"

        }

      ],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "vUdbskYE2d87",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 2\n",

        "---------\n",

        "\n",

        "Let's verify that the data still looks good. Displaying a sample of the labels and images from the ndarray. Hint: you can use matplotlib.pyplot.\n",

        "\n",

        "---"

      ]

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "cYznx5jUwzoO",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 3\n",

        "---------\n",

        "Another check: we expect the data to be balanced across classes. Verify that.\n",

        "\n",

        "---"

      ]

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "LA7M7K22ynCt",

        "colab_type": "text"

      },

      "source": [

        "Merge and prune the training data as needed. Depending on your computer setup, you might not be able to fit it all in memory, and you can tune `train_size` as needed. The labels will be stored into a separate array of integers 0 through 9.\n",

        "\n",

        "Also create a validation dataset for hyperparameter tuning."

      ]

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "s3mWgZLpyuzq",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          },

          "output_extras": [

            {

              "item_id": 1

            }

          ]

        },

        "cellView": "both",

        "executionInfo": {

          "elapsed": 411281,

          "status": "ok",

          "timestamp": 1444485897869,

          "user": {

            "color": "#1FA15D",

            "displayName": "Vincent Vanhoucke",

            "isAnonymous": false,

            "isMe": true,

            "permissionId": "05076109866853157986",

            "photoUrl": "//lh6.googleusercontent.com/-cCJa7dTDcgQ/AAAAAAAAAAI/AAAAAAAACgw/r2EZ_8oYer4/s50-c-k-no/photo.jpg",

            "sessionId": "2a0a5e044bb03b66",

            "userId": "102167687554210253930"

          },

          "user_tz": 420

        },

        "outputId": "8af66da6-902d-4719-bedc-7c9fb7ae7948"

      },

      "source": [

        "def make_arrays(nb_rows, img_size):\n",

        " if nb_rows:\n",

        " dataset = np.ndarray((nb_rows, img_size, img_size), dtype=np.float32)\n",

        " labels = np.ndarray(nb_rows, dtype=np.int32)\n",

        " else:\n",

        " dataset, labels = None, None\n",

        " return dataset, labels\n",

        "\n",

        "def merge_datasets(pickle_files, train_size, valid_size=0):\n",

        " num_classes = len(pickle_files)\n",

        " valid_dataset, valid_labels = make_arrays(valid_size, image_size)\n",

        " train_dataset, train_labels = make_arrays(train_size, image_size)\n",

        " vsize_per_class = valid_size // num_classes\n",

        " tsize_per_class = train_size // num_classes\n",

        " \n",

        " start_v, start_t = 0, 0\n",

        " end_v, end_t = vsize_per_class, tsize_per_class\n",

        " end_l = vsize_per_class+tsize_per_class\n",

        " for label, pickle_file in enumerate(pickle_files): \n",

        " try:\n",

        " with open(pickle_file, 'rb') as f:\n",

        " letter_set = pickle.load(f)\n",

        " # let's shuffle the letters to have random validation and training set\n",

        " np.random.shuffle(letter_set)\n",

        " if valid_dataset is not None:\n",

        " valid_letter = letter_set[:vsize_per_class, :, :]\n",

        " valid_dataset[start_v:end_v, :, :] = valid_letter\n",

        " valid_labels[start_v:end_v] = label\n",

        " start_v += vsize_per_class\n",

        " end_v += vsize_per_class\n",

        " \n",

        " train_letter = letter_set[vsize_per_class:end_l, :, :]\n",

        " train_dataset[start_t:end_t, :, :] = train_letter\n",

        " train_labels[start_t:end_t] = label\n",

        " start_t += tsize_per_class\n",

        " end_t += tsize_per_class\n",

        " except Exception as e:\n",

        " print('Unable to process data from', pickle_file, ':', e)\n",

        " raise\n",

        " \n",

        " return valid_dataset, valid_labels, train_dataset, train_labels\n",

        " \n",

        " \n",

        "train_size = 200000\n",

        "valid_size = 10000\n",

        "test_size = 10000\n",

        "\n",

        "valid_dataset, valid_labels, train_dataset, train_labels = merge_datasets(\n",

        " train_datasets, train_size, valid_size)\n",

        "_, _, test_dataset, test_labels = merge_datasets(test_datasets, test_size)\n",

        "\n",

        "print('Training:', train_dataset.shape, train_labels.shape)\n",

        "print('Validation:', valid_dataset.shape, valid_labels.shape)\n",

        "print('Testing:', test_dataset.shape, test_labels.shape)"

      ],

      "outputs": [

        {

          "output_type": "stream",

          "text": [

            "Training (200000, 28, 28) (200000,)\n",

            "Validation (10000, 28, 28) (10000,)\n",

            "Testing (10000, 28, 28) (10000,)\n"

          ],

          "name": "stdout"

        }

      ],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "GPTCnjIcyuKN",

        "colab_type": "text"

      },

      "source": [

        "Next, we'll randomize the data. It's important to have the labels well shuffled for the training and test distributions to match."

      ]

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "6WZ2l2tN2zOL",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          }

        },

        "cellView": "both"

      },

      "source": [

        "def randomize(dataset, labels):\n",

        " permutation = np.random.permutation(labels.shape[0])\n",

        " shuffled_dataset = dataset[permutation,:,:]\n",

        " shuffled_labels = labels[permutation]\n",

        " return shuffled_dataset, shuffled_labels\n",

        "train_dataset, train_labels = randomize(train_dataset, train_labels)\n",

        "test_dataset, test_labels = randomize(test_dataset, test_labels)\n",

        "valid_dataset, valid_labels = randomize(valid_dataset, valid_labels)"

      ],

      "outputs": [],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "puDUTe6t6USl",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 4\n",

        "---------\n",

        "Convince yourself that the data is still good after shuffling!\n",

        "\n",

        "---"

      ]

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "tIQJaJuwg5Hw",

        "colab_type": "text"

      },

      "source": [

        "Finally, let's save the data for later reuse:"

      ]

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "QiR_rETzem6C",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          }

        },

        "cellView": "both"

      },

      "source": [

        "pickle_file = os.path.join(data_root, 'notMNIST.pickle')\n",

        "\n",

        "try:\n",

        " f = open(pickle_file, 'wb')\n",

        " save = {\n",

        " 'train_dataset': train_dataset,\n",

        " 'train_labels': train_labels,\n",

        " 'valid_dataset': valid_dataset,\n",

        " 'valid_labels': valid_labels,\n",

        " 'test_dataset': test_dataset,\n",

        " 'test_labels': test_labels,\n",

        " }\n",

        " pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)\n",

        " f.close()\n",

        "except Exception as e:\n",

        " print('Unable to save data to', pickle_file, ':', e)\n",

        " raise"

      ],

      "outputs": [],

      "execution_count": 0

    },

    {

      "cell_type": "code",

      "metadata": {

        "id": "hQbLjrW_iT39",

        "colab_type": "code",

        "colab": {

          "autoexec": {

            "startup": false,

            "wait_interval": 0

          },

          "output_extras": [

            {

              "item_id": 1

            }

          ]

        },

        "cellView": "both",

        "executionInfo": {

          "elapsed": 413065,

          "status": "ok",

          "timestamp": 1444485899688,

          "user": {

            "color": "#1FA15D",

            "displayName": "Vincent Vanhoucke",

            "isAnonymous": false,

            "isMe": true,

            "permissionId": "05076109866853157986",

            "photoUrl": "//lh6.googleusercontent.com/-cCJa7dTDcgQ/AAAAAAAAAAI/AAAAAAAACgw/r2EZ_8oYer4/s50-c-k-no/photo.jpg",

            "sessionId": "2a0a5e044bb03b66",

            "userId": "102167687554210253930"

          },

          "user_tz": 420

        },

        "outputId": "b440efc6-5ee1-4cbc-d02d-93db44ebd956"

      },

      "source": [

        "statinfo = os.stat(pickle_file)\n",

        "print('Compressed pickle size:', statinfo.st_size)"

      ],

      "outputs": [

        {

          "output_type": "stream",

          "text": [

            "Compressed pickle size: 718193801\n"

          ],

          "name": "stdout"

        }

      ],

      "execution_count": 0

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "gE_cRAQB33lk",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 5\n",

        "---------\n",

        "\n",

        "By construction, this dataset might contain a lot of overlapping samples, including training data that's also contained in the validation and test set! Overlap between training and test can skew the results if you expect to use your model in an environment where there is never an overlap, but are actually ok if you expect to see training samples recur when you use it.\n",

        "Measure how much overlap there is between training, validation and test samples.\n",

        "\n",

        "Optional questions:\n",

        "- What about near duplicates between datasets? (images that are almost identical)\n",

        "- Create a sanitized validation and test set, and compare your accuracy on those in subsequent assignments.\n",

        "---"

      ]

    },

    {

      "cell_type": "markdown",

      "metadata": {

        "id": "L8oww1s4JMQx",

        "colab_type": "text"

      },

      "source": [

        "---\n",

        "Problem 6\n",

        "---------\n",

        "\n",

        "Let's get an idea of what an off-the-shelf classifier can give you on this data. It's always good to check that there is something to learn, and that it's a problem that is not so trivial that a canned solution solves it.\n",

        "\n",

        "Train a simple model on this data using 50, 100, 1000 and 5000 training samples. Hint: you can use the LogisticRegression model from sklearn.linear_model.\n",

        "\n",

        "Optional question: train an off-the-shelf model on all the data!\n",

        "\n",

        "---"

      ]

    }

  ]

}







