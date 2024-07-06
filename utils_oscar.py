import numpy as np

'''
    brief: Calcul de la distance en pixel correspondante à la distance entre les deux pics de fréquences
        On passe de l'espace fréquentiel à l'espace spatial

    @param freq_dist: distance dans l'espace fréquentiel entre les deux pics maximums
    @param magnitude_1d: array de magnitude 1D de fréquences
'''
def freq_dist_to_pixel_dist(freq_dist, magnitude_1d, log=True):
    pixel_dist = 1/ ( freq_dist / magnitude_1d.shape[0] )
    if log:
        print("La distance en pixel est de: %.2f\n" % pixel_dist)
    return pixel_dist


'''
    brief: Calcul de la vitesse du météore en pixel par secondes

    @param pixel_dist: distance en pixel entre les deux pics maximums
    @param refresh_duration: durée de rafraichissement en secondes
'''
def pixel_dist_to_pixel_speed(pixel_dist, refresh_duration=100, log=True):
    meteor_speed_ms = pixel_dist / refresh_duration
    meteor_speed_s = meteor_speed_ms * 1000
    if log:
        print("(Le taux de rafrachissement est de %.1f ms)" % refresh_duration)
        print("La vitesse est donc de: %.2f pixel/ms" % meteor_speed_ms)
        print("                        %.2f pixel/s\n" % meteor_speed_s)
    return meteor_speed_s

'''
    brief: Calcul de la vitesse réelle du météore en m/s et km/h

    @param meteor_speed_s: vitesse du météore en pixel par secondes
    @param dist_per_pixel: distance en mètre par pixel (valeur par défaut 1000 mètres)
'''
def pixel_speed_to_real_speed(meteor_speed_s, dist_per_pixel=1000, log=True):
    real_speed = meteor_speed_s * dist_per_pixel
    if log:
        print("(La distance par pixel est de %.2f m)" % dist_per_pixel)
        print("La vitesse réelle est donc de: %.2f m/s" % real_speed)
        print("                               %.2f km/h" % (real_speed * 3.6))
        print("                               %.2f km/s" % (real_speed / 1000))
    return real_speed


def meteor_speed(magnitude_1d, log=True):
    magnitude_1d_begin = np.insert(magnitude_1d, 0, magnitude_1d[0]) # 0 begin
    magnitude_1d_end   = np.append(magnitude_1d, magnitude_1d[-1]) # 0 end

    derivate = magnitude_1d_end - magnitude_1d_begin
    supremums = np.all([derivate[:-1] > 0, derivate[1:] < 0], axis=0)

    x_supremums = np.where(supremums)[0]
    y_supremums = np.array(magnitude_1d[supremums])

    indexes = np.flip(np.argsort(y_supremums))

    center_index = x_supremums[indexes[0]]
    max_index = x_supremums[indexes[1]]
    dist_freq = abs(center_index - max_index)

    dist_pixel = freq_dist_to_pixel_dist(dist_freq, magnitude_1d, log=log)

    pixel_speed = pixel_dist_to_pixel_speed(dist_pixel, log=log)

    real_speed = pixel_speed_to_real_speed(pixel_speed, log=log)

    return real_speed