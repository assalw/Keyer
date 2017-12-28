import av
import numpy as np
import pygame
import pygame.surfarray as surfarray

from skimage.segmentation import slic, mark_boundaries

def render(video):

    surface = None

    lastTime, currentTime = pygame.time.get_ticks(), 0

    # Decode video and apply keying algorithm
    for packet in video.demux():
        for frame in packet.decode():
            if type(frame) == av.video.frame.VideoFrame:
                img = frame.to_image()  # PIL/Pillow image
                array = np.asarray(img)  # numpy array
                array = np.rot90(array)
                array = np.flipud(array)

                # TODO: Keyer
                segments = slic(array, slic_zero=True)
                array = mark_boundaries(array, segments, color=[5, 5, 5])
                array = array * 255

                # Create surface if None
                if surface is None:
                    surface = pygame.display.set_mode(array.shape[:2], 0, 32)

                # Write array to surface
                surfarray.blit_array(surface, array)

                # Run at 25 frames per second
                currentTime = pygame.time.get_ticks()
                if (lastTime + 40) < currentTime:
                    pygame.display.update()
                else:
                    pygame.time.delay((lastTime + 40) - currentTime)
                    pygame.display.update()

                lastTime = currentTime

def main():
    # set up pygame
    pygame.init()

    # Open video file
    video = av.open('video/a.mp4')

    # Start render loop
    render(video)

if __name__ == "__main__":
    main()