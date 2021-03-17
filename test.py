import os
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from models.model_select import create_model
from util.visualizer import Visualizer
from util import html

opt 				= TestOptions().parse()
opt.nThreads 		= 1   # test code only supports nThreads = 1
opt.batchSize 		= 1  # test code only supports batchSize = 1
opt.serial_batches 	= True  # no shuffle
opt.no_flip 		= True  # no flip

data_loader = CreateDataLoader(opt)
dataset 	= data_loader.load_data()
model 		= create_model(opt)
visualizer 	= Visualizer(opt)
# create website
#web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
#webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))
web_dir = os.path.join(opt.results_dir, '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment, Phase = %s, Epoch = %s' % (opt.phase, opt.which_epoch))
# test
avgPSNR = 0.0
avgSSIM = 0.0
counter = 0

for i, data in enumerate(dataset):
	if i >= opt.how_many:
		break
	counter = i
	model.set_input(data)
	model.test()
	visuals = model.get_current_visuals()
	#avgPSNR += PSNR(visuals['fake_B'],visuals['real_B'])
	#pilFake = Image.fromarray(visuals['fake_B'])
	#pilReal = Image.fromarray(visuals['real_B'])
	#avgSSIM += SSIM(pilFake).cw_ssim_value(pilReal)
	img_path = model.get_image_paths()
	print('process image... %s' % img_path)
	visualizer.save_images(webpage, visuals, img_path)
	
#avgPSNR /= counter
#avgSSIM /= counter
#print('PSNR = %f, SSIM = %f' % (avgPSNR, avgSSIM))

webpage.save()
